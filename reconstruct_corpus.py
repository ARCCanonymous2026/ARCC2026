import os
import time
import pandas as pd
import praw
from tqdm import tqdm


# 1️ USER MUST INSERT CREDENTIALS
REDDIT_CLIENT_ID = "YOUR_CLIENT_ID"
REDDIT_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDDIT_USER_AGENT = "ARCC-reconstruction"

# 2️ PATH CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "corpus", "ARCC_anonymized.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "corpus", "ARCC_reconstructed.csv")


# 3️ INITIALIZE REDDIT API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# 4️ Load data
df = pd.read_csv(INPUT_PATH)


# 5️ Reconstruction function
def reconstruct_segment(row):
    """
    Fetch comment or post text and extract segment using offsets.
    Returns (full_comment_text, segment_text) or (None, None) if unavailable.
    """
    comment_id = str(row["comment_id"])
    start = int(row["segment_start"])
    end = int(row["segment_end"])

    # Detect Reddit prefix
    if comment_id.startswith("t1_") or comment_id.startswith("t3_"):
        raw_id = comment_id[3:]
        prefix = comment_id[:3]
    else:
        raw_id = comment_id
        prefix = "t3_" if int(row.get("depth", 1)) == 0 else "t1_"

    try:
        if prefix == "t3_":
            submission = reddit.submission(id=raw_id)
            text = (submission.title or "") + "\n" + (submission.selftext or "")
        else:
            comment = reddit.comment(id=raw_id)
            text = comment.body

        if text in ["[deleted]", "[removed]", None]:
            return None, None

        segment = text[start:end]
        return text, segment

    except Exception as e:
        print(f"Error fetching {comment_id}: {e}")
        return None, None


# 6️ Reconstruct corpus
full_comments = []
segments = []

for _, row in tqdm(df.iterrows(), total=len(df)):
    comment_text, segment_text = reconstruct_segment(row)

    full_comments.append(comment_text)
    segments.append(segment_text)

    # Be polite to Reddit API
    time.sleep(0.1)

# Add columns to dataframe
df["Comment"] = full_comments
df["Segment"] = segments


# 7️ Save output
df.to_csv(OUTPUT_PATH, index=False)

print("\nReconstruction completed.")
print(f"Output saved to: {OUTPUT_PATH}")