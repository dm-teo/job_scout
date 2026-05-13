select distinct on (trim(lower(job_title)), left(trim(lower(description)), 100)) job_title, description, link, is_remote, seniority_label
from {{ ref('stg_jobs') }}
    order by trim(lower(job_title)), left(trim(lower(description)), 100), link