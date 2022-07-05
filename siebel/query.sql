select
    x.par_duns_num as tipoDoc,
    x.duns_num as nroDoc,
    w.fst_name as nombres,
    w.last_name as apellidos,
    trunc(w.birth_dt) as fechaNacim,
    w.job_title as job,
    x.created as creacionRegCliente,
    x.active_flg as clienteActivo,
    w.ondemand_sync_flg as demanda,
    y.billacct_id as cuentaBscs,
    x.master_ou_id as padre,
    cf.x_prod_line as tipo
from
    siebel.s_contact w,
    siebel.s_org_ext x,
    siebel.s_billacct_org y,
    siebel.s_ins_billacct cf
where
    w.row_id = x.pr_con_id
    and x.master_ou_id = y.ou_id
    and x.active_flg = 'Y'
    and x.par_duns_num = '{{{tid}}}'
    and x.duns_num = '{{{numid}}}'
    and cf.billacct_num = y.billacct_id
    and cf.x_prod_line = 'Postpago'
    and cf.ACCT_STATUS = 'Activo'