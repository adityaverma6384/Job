import re
import json

# Career clusters with skills
career_clusters = {
    'Architecture and Construction': ['architect', 'architecture', 'building', 'construction', 'design', 'engineer',
                                     'structural', 'drafting', 'blueprint', 'project management'],
    'Arts, Audio/Video Technology and Communications': ['art', 'audio', 'communication', 'design', 'media',
                                                       'technology', 'visual', 'graphic design', 'video production',
                                                       'photography'],
    'Business Management and Administration': ['administration', 'business', 'management', 'finance', 'operations',
                                               'strategy', 'leadership', 'entrepreneurship', 'business analysis',
                                               'project management'],
    'Education and Training': ['education', 'instructor', 'learning', 'teaching', 'training', 'curriculum', 'student',
                               'e-learning', 'educational technology', 'instructional design'],
    'Finance': ['accounting', 'finance', 'investment', 'banking', 'financial', 'analysis', 'tax', 'auditing',
                'financial planning', 'risk management'],
    'Government and Public Administration': ['government', 'public administration', 'policy', 'regulation',
                                             'public service', 'political', 'legislation', 'public policy',
                                             'government relations', 'budgeting'],
    'Health Science': ['healthcare', 'medical', 'nursing', 'pharmaceutical', 'research', 'patient', 'clinical',
                       'health informatics', 'healthcare administration', 'epidemiology'],
    'Hospitality and Tourism': ['hospitality', 'tourism', 'hotel', 'restaurant', 'customer service', 'event',
                                'catering', 'travel', 'hospitality management', 'event planning'],
    'Human Services': ['social work', 'counseling', 'community', 'nonprofit', 'advocacy', 'youth', 'family',
                       'case management', 'social justice', 'volunteer coordination'],
    'Information Technology': ['information technology', 'software', 'programming', 'network', 'database',
                               'cybersecurity', 'web', 'data analysis', 'cloud computing', 'IT project management'],
    'Law, Public Safety, Corrections, and Security': ['law', 'public safety', 'security', 'criminal justice',
                                                     'legal', 'enforcement', 'investigation', 'court procedures',
                                                     'emergency management', 'cybersecurity'],
    'Manufacturing': ['manufacturing', 'production', 'assembly', 'supply chain', 'quality control', 'engineering',
                      'operations', 'lean manufacturing', 'industrial engineering', 'product development'],
    'Marketing, Sales, and Service': ['marketing', 'sales', 'customer', 'advertising', 'branding', 'market research',
                                      'customer service', 'digital marketing', 'sales management', 'CRM'],
    'Science, Technology, Engineering, and Mathematics': ['science', 'technology', 'engineering', 'mathematics',
                                                         'research', 'data', 'analysis', 'machine learning',
                                                         'data science', 'quantitative analysis'],
    'Transportation, Distribution, and Logistics': ['transportation', 'logistics', 'supply chain', 'warehouse',
                                                    'fleet', 'shipping', 'inventory', 'procurement',
                                                    'international trade', 'demand planning'],
    'Other Services': ['service', 'maintenance', 'repair', 'personal care', 'beauty', 'wellness', 'cleaning',
                       'landscaping', 'hair styling', 'pet grooming']
}

# Read the text file
with open('output.txt', 'r', encoding='utf-8') as file:
    job_data = file.read()

# Extract job summaries and requirements using regex
job_regex = r"Summary for Job (\d+):\n(.*?)\n\nRequirements for Job \1:\n(.*?)\n\n"
jobs = re.findall(job_regex, job_data, re.DOTALL)

# Cluster jobs based on skills
clustered_jobs = {}
for job in jobs:
    job_num = job[0]
    summary = job[1]
    requirements = job[2]

    matched_cluster = None
    max_match_count = 0

    # Find the cluster with the most matching skills
    for cluster, skills in career_clusters.items():
        match_count = sum(1 for skill in skills if skill.lower() in requirements.lower())
        if match_count > max_match_count:
            matched_cluster = cluster
            max_match_count = match_count

    if matched_cluster is not None:
        # Add the job to the matched cluster
        if matched_cluster in clustered_jobs:
            clustered_jobs[matched_cluster].append({'job_num': job_num, 'summary': summary, 'requirements': requirements})
        else:
            clustered_jobs[matched_cluster] = [{'job_num': job_num, 'summary': summary, 'requirements': requirements}]
    else:
        # Add the job to the 'Other Services' cluster
        if 'Other Services' in clustered_jobs:
            clustered_jobs['Other Services'].append({'job_num': job_num, 'summary': summary, 'requirements': requirements})
        else:
            clustered_jobs['Other Services'] = [{'job_num': job_num, 'summary': summary, 'requirements': requirements}]

# Save the clustered jobs as a JSON file
with open('clustered_jobs.json', 'w') as outfile:
    json.dump(clustered_jobs, outfile, indent=4)

# Calculate cluster statistics
cluster_stats = {}

for cluster, jobs in clustered_jobs.items():
    cluster_stats[cluster] = len(jobs)

# Save the cluster statistics as a JSON file
with open('cluster_stats.json', 'w') as outfile:
    json.dump(cluster_stats, outfile, indent=4)
