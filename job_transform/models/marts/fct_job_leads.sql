SELECT DISTINCT ON (job_title, description) job_title, description, link, is_remote, seniority_label
from {{ ref('stg_jobs') }}
    order by job_title, description