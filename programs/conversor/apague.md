```sql





select * from (
    select DISTINCT(M.ID_MANIF) /* concluídas */
        FROM MANIFESTACAO M inner join
                TRAMITACAO T ON M.ID_MANIF = T.COD_MANIFESTACAO
        WHERE T.DATA_INICIO between to_date('01/01/2019 00:00:00','dd/mm/yyyy hh24:mi:ss') 
                and to_date('31/12/2019 23:59:59', 'dd/mm/yyyy hh24:mi:ss')
                AND T.COD_DESCRICAO_SITUACAO = 190
                and M.ID_MANIF NOT IN (311124,311163,311307,311367,311399,311402,311412,312794,313550,313827,314236,311413,314099,315675,314095)
    union
    select DISTINCT(M.ID_MANIF) /* arquivadas */
                    FROM MANIFESTACAO M inner join
                    TRAMITACAO T ON M.ID_MANIF = T.COD_MANIFESTACAO
                    WHERE 
                        t.cod_descricao_situacao = 199
                        AND t.data_inicio between to_date('01/01/2019 00:00:00','dd/mm/yyyy hh24:mi:ss') 
                        and to_date('31/12/2019 23:59:59', 'dd/mm/yyyy hh24:mi:ss')                
                        and M.ID_MANIF NOT IN (311124,311163,311307,311367,311399,311402,311412,312794,313550,313827,314236,311413,314099,315675,314095)
) juntas
where juntas.ID_MANIF not in (
    select DISTINCT(M.ID_MANIF) /* total */
       FROM MANIFESTACAO M inner join
            TRAMITACAO T ON M.ID_MANIF = T.COD_MANIFESTACAO
            -- left join (

            -- ) amais on amais.ID_MANIF = M.ID_MANIF
       WHERE M.DATA_MANIF between to_date('01/01/2019 00:00:00','dd/mm/yyyy hh24:mi:ss') 
             and to_date('31/12/2019 23:59:59', 'dd/mm/yyyy hh24:mi:ss')
             and M.ID_MANIF NOT IN (311124,311163,311307,311367,311399,311402,311412,312794,313550,313827,314236,311413,314099,315675,314095)
)

gerar download em 

classificação
fora do período
166



```