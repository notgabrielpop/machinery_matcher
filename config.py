# Configuration file for Machinery Matcher

# STEP 1: Paste your Anthropic API key here
ANTHROPIC_API_KEY = "sk-ant-your-key-here"  # REPLACE THIS!

# STEP 2: Your CSV file name
CSV_FILE_PATH = "prospects.csv"  # Change to your actual file name

# STEP 3: How many top providers?
TOP_N_PROVIDERS = 10

# STEP 4: Maximum prospects to analyze
MAX_PROSPECTS_TO_ANALYZE = 1500

# STEP 5: Enable website scraping?
# False = Fast (30 min, $15-30, 65% accuracy)
# True = Accurate (2-3 hours, $50-75, 90% accuracy)
ENABLE_WEB_SCRAPING = False  # Start with False

# STEP 6: Filter by technology?
# None = All prospects
# "injection" = Only injection molding
# "extrusion" = Only extrusion
# "blow_molding" = Only blow molding
# etc.
FILTER_BY_TECHNOLOGY = None  # Start with None

# Performance settings
BATCH_SIZE = 50
USE_CACHE = True
PARALLEL_PROCESSING = True