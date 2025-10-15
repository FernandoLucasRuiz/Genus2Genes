def taxid_from_genus(genus):
    r = requests.get(f"{"https://www.ebi.ac.uk/ena/taxonomy/rest/scientific-name/"}{genus}", headers={"Accept": "application/json"})
    r.raise_for_status()

    for hit in r.json():
        if hit.get("rank") == "genus":
            return hit["taxId"]
    raise ValueError(f"No se encontró el género {genus}")

def species_from_genus(genus):
    taxid = taxid_from_genus(genus)
    xml = requests.get(f"{"https://www.ebi.ac.uk/ena/browser/api/xml/"}{taxid}").content
    root   = ET.fromstring(xml)

    species = []
    for tax in root.findall(".//taxon"):
        rank = tax.get("rank") or tax.findtext("rank")
        if rank == "species":
            species.append({
                "taxId": tax.get("taxId") or tax.findtext("taxId"),
                "name":  tax.get("scientificName") or tax.findtext("scientificName")
            })
    return species

def get_pmids(taxon, specie, num_salida):
    Entrez.email = 'fernando.lucas@um.es'

    query = f"{taxon} AND {specie}"

    date_range = '("1950/01/01"[Date - Create] : "2024/12/31"[Date - Create])'

    full_query = query + ' AND ' + date_range
    
    search_handle = Entrez.esearch(db="pubmed", 
                                   term=full_query, 
                                   retmax=num_salida
                                   )
    search_results = Entrez.read(search_handle)
    search_handle.close()
    
    pmids = search_results["IdList"]
    return pmids

def fetch_article_details(pmids):

    handle = Entrez.efetch(db="pubmed", 
                           id=",".join(pmids), 
                           rettype="medline", 
                           retmode="xml")
    records = Entrez.read(handle)
    
    articles = []
    for record in records['PubmedArticle']:
        article = {
            "title": record.get("MedlineCitation", {}).get("Article", {}).get("ArticleTitle", ""),
            "authors": [author.get('ForeName', '') + ' ' + author.get('LastName', '') for author in record.get("MedlineCitation", {}).get("Article", {}).get("AuthorList", [])],
            "abstract": "".join(record.get("MedlineCitation", {}).get("Article", {}).get("Abstract", {}).get("AbstractText", []))
        }
        articles.append(article)
    handle.close()
    return articles

def get_genes_pubtator(pmids):
    
    url = "https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/biocjson"
    params = {
        "pmids": ",".join(pmids), 
        "full": "true"
    }

    response = requests.get(url, params=params)
    time.sleep(1) 

    if response.status_code != 200:
        print(f"Error al recuperar datos: {response.status_code}")
        return {}, pd.DataFrame()

    data = response.json()  

    secciones_interes = {"TITLE", "ABSTRACT", "INTRO", "METHODS", "RESULTS", "TABLE", "FIG"}
    genes_extraidos = []

    for article in data.get("PubTator3", []):
        pmid = article.get("_id", "Desconocido").split("|")[0] 

        for passage in article.get("passages", []):
            section_type = passage.get("infons", {}).get("section_type", "").upper()

            for annotation in passage.get("annotations", []):
                if annotation.get("infons", {}).get("type") == "Gene":
                    genes_extraidos.append({
                        "PMID": pmid,
                        "Gene_ID": annotation.get("infons", {}).get("identifier"),
                        "Gene_Name": annotation.get("infons", {}).get("name"),
                        "Section": section_type
                    })

    df_genes = pd.DataFrame(genes_extraidos)

    return df_genes

