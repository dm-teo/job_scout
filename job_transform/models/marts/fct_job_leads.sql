SELECT DISTINCT ON (link) link, job_title, is_remote, seniority_label, description
from {{ ref('stg_jobs') }}
    order by link