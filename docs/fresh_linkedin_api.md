# Fresh LinkedIn Profile Data — search-jobs endpoint

**Base URL**  
`https://fresh-linkedin-profile-data.p.rapidapi.com/search-jobs`

**Required headers**
```http
X-RapidAPI-Key: $RAPIDAPI_KEY
X-RapidAPI-Host: fresh-linkedin-profile-data.p.rapidapi.com
```

**Example cURL (works)**
curl --request POST \
	--url https://fresh-linkedin-profile-data.p.rapidapi.com/search-jobs \
	--header 'Content-Type: application/json' \
	--header 'x-rapidapi-host: fresh-linkedin-profile-data.p.rapidapi.com' \
	--header 'x-rapidapi-key: f98d2f5769mshe0d2e9743c3bfafp1db82cjsn7efaf19497db' \
	--data '{"keywords":"financial advisor","geo_code":101452733,"date_posted":"Past 24 hours","experience_levels":[],"company_ids":[],"title_ids":[],"onsite_remotes":[],"functions":[],"industries":["Financial Services"],"job_types":[],"sort_by":"Most relevant","easy_apply":"false","under_10_applicants":"false","start":0}'


# Fresh LinkedIn Profile Data — search-decision-makers endpoint

**Base URL**  
`https://fresh-linkedin-profile-data.p.rapidapi.com/search-decision-makers`

**Required headers**
```http
X-RapidAPI-Key: $RAPIDAPI_KEY
X-RapidAPI-Host: fresh-linkedin-profile-data.p.rapidapi.com
```

**Example cURL (works)**
curl --request POST \
	--url https://fresh-linkedin-profile-data.p.rapidapi.com/search-decision-makers \
	--header 'Content-Type: application/json' \
	--header 'x-rapidapi-host: fresh-linkedin-profile-data.p.rapidapi.com' \
	--header 'x-rapidapi-key: f98d2f5769mshe0d2e9743c3bfafp1db82cjsn7efaf19497db' \
	--data '{"company_ids":[892970],"title_keywords":["CEO","Founder","Co-Founder","Owner","CFO","Managing Director","Director","Practice Manager","General Manager"],"geo_codes":[101452733],"limit":"5"}'