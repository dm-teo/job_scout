select distinct on (link)
    job_title,
    description,
    link,
    current_date as load_date,
    is_remote,
    seniority_label
from {{ ref('stg_jobs') }}
order by link, job_title