select initcap(title) as job_title, is_remote, link, description,
    case
        when is_junior = True then 'Junior'
        else 'Not Specified'
    end as seniority_label
from {{ source('raw_jobs_data', 'job_scout_db') }}
