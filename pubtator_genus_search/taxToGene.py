results_list = []

for tax in lines_clean:

     print("Genus: ", tax)

     species = species_from_genus(tax)
     names_species = [sp["name"] for sp in species]

     for sp in names_species:

          pmids = get_pmids(sp, '(Human OR Homo sapiens)', 100000)
          
          start2 = time.time()
          if(len(pmids) != 0):

               if len(pmids) > 100:
                    for i in range(0, len(pmids), 100):
                         batch_pmids = pmids[i:i + 100] 
                         df_genes = get_genes_pubtator(batch_pmids)

                         if not df_genes.empty:
                              df_genes["Taxon"] = sp
                              results_list.append(df_genes)
               else:
                    df_genes = get_genes_pubtator(pmids)

                    if not df_genes.empty:
                         df_genes["Taxon"] = sp
                         results_list.append(df_genes)

df_results = pd.concat(results_list, ignore_index=True) if results_list else pd.DataFrame()
