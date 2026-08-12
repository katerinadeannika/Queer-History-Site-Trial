# Chapter source audit

- Chapters audited: 14
- Unique linked URL/DOI sources in chapters: 167
- Unique linked URL/DOI sources in bibliography documents: 224
- Chapter sources missing from both bibliography documents: 31
- Exact normalized source duplicates across bibliography documents: 12

## Missing linked sources
### chapter-02-1880s.html
- `https://chicago.universitypressscholarship.com/view/10.7208/chicago/9780226389288.001.0001/upso-9780226389257-chapter-2`
- `https://parliament.uk/about/living-heritage/transformingsociety/private-lives/relationships/collections1/sexual-offences-act-1967/1885-labouchere-amendment`

### chapter-03-1890s.html
- `https://parliament.uk/about/living-heritage/transformingsociety/private-lives/relationships/collections1/sexual-offences-act-1967/1885-labouchere-amendment`

### chapter-04-1900s.html
- `https://britannica.com/biography/Magnus-Hirschfeld`
- `https://legacyprojectchicago.org/milestone/scientific-humanitarian-committee`
- `https://musea.fr/s/musea/page/creating-yourself`

### chapter-05-1910s.html
- `https://archive.org/search?query=World%20War%20I%20mediatype%3Amovies`
- `https://digitalcommons.mtu.edu/cgi/viewcontent.cgi?article=1024&context=ww1cc-symposium`
- `https://playbill.com/article/the-history-of-the-all-female-japanese-theatre-troupe-that-is-bringing-chicago-to-nyc`

### chapter-06-1920s.html
- `https://archive.org/search?query=Die%20Freundin%20Berlin`
- `https://loc.gov/photos?q=Harlem`

### chapter-07-1930s.html
- `https://archive.org/search?query=Berlin%201930s%20mediatype%3Amovies`
- `https://archive.org/search?query=M%C3%A4dchen%20in%20Uniform`
- `https://archive.org/search?query=Spanish%20Civil%20War%20mediatype%3Amovies`
- `https://loc.gov/photos?q=Great+Depression`

### chapter-08-1940s.html
- `https://archive.org/search?query=Universal%20Newsreel`
- `https://archive.org/search?query=World%20War%20II%20mediatype%3Amovies`
- `https://auschwitz.org/en/education/e-learning/podcast/paragraph-175-prisoners-in-auschwitz`
- `https://loc.gov/photos?q=World+War+II`

### chapter-09-1950s.html
- `https://archive.org/search?query=London%201950s%20mediatype%3Amovies`
- `https://archive.org/search?query=New%20York%201950s%20mediatype%3Amovies`
- `https://archive.org/search?query=ONE%20Magazine`
- `https://archive.org/search?query=Paris%201890s%20film%20footage`
- `https://archive.org/search?query=The%20Ladder%20Daughters%20of%20Bilitis`

### chapter-10-1960s.html
- `https://archive.org/search?query=London%201960s%20mediatype%3Amovies`
- `https://archive.org/search?query=New%20York%201960s%20mediatype%3Amovies`
- `https://loc.gov/photos?q=1960s+protest`

### chapter-11-threads.html
- `https://archive.org/advancedsearch.php`
- `https://si.edu/search/collection-images`

### chapter-12-end-material.html
- `https://archive.org/advancedsearch.php`
- `https://si.edu/search/collection-images`

## Duplicate bibliography sources
- `https://archives.gov/publications/prologue/2016/summer/lavender.html` — bibliography.html, chapter-14-bibliography.html
- `https://arolsen-archives.org/en/news/the-long-road-to-legal-reform-2` — bibliography.html, chapter-14-bibliography.html
- `https://districtsix.co.za/project/kewpie-daughter-of-district-six` — bibliography.html, chapter-14-bibliography.html
- `https://dumaurier.org/mobile/menu_page.php?id=180` — bibliography.html, chapter-14-bibliography.html
- `https://encyclopedia.ushmm.org/content/en/article/paragraph-175-and-the-nazi-campaign-against-homosexuality` — bibliography.html, chapter-14-bibliography.html
- `https://encyclopedia.ushmm.org/content/en/timeline-event/holocaust/1933-1938/revision-of-paragraph-175` — bibliography.html, chapter-14-bibliography.html
- `https://gala.co.za/projects-and-programmes/kewpie` — bibliography.html, chapter-14-bibliography.html
- `https://help.archive.org/help/prelinger-archive` — bibliography.html, chapter-14-bibliography.html
- `https://humandignitytrust.org/lgbt-the-law/a-history-of-criminalisation` — bibliography.html, chapter-14-bibliography.html
- `https://loc.gov/collections/chronicling-america/about-this-collection` — bibliography.html, chapter-14-bibliography.html
- `https://loc.gov/collections/national-jukebox/about-this-collection` — bibliography.html, chapter-14-bibliography.html
- `https://rosenbach.squarespace.com/s/The-Mercedes-de-Acosta-Papers.pdf` — bibliography.html, chapter-14-bibliography.html

## Method and limits
- Compares normalized external URLs and DOI strings found in chapter HTML with those found in `bibliography.html` and `chapter-14-bibliography.html`.
- Removes URL fragments and normalizes case, `www.`, and trailing slashes for comparison.
- Does not evaluate unlinked prose citations that contain no URL or DOI.
