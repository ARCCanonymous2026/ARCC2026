# Annotated Reddit Conversation Corpus (ARCC) – Anonymous Submission

## Overview

The **Annotated Reddit Conversation Corpus (ARCC)** is a collection of Reddit conversations, **segmented and annotated** for both:

1. **Speech Acts** – capturing the communicative function of each segment (e.g., assertion, question, assessment, advise, expressive).  
2. **Functional Dependence Relations (FDRs)** – representing how segments relate to one another in the conversation, encoding dependencies such as agreement, disagreement, answer, or request for clarification.

The corpus is designed for the **study of subjectivity in online discourse**. Specifically, it allows researchers to investigate how **subjective expressions** at the speech act level influence conversational dynamics, as captured by FDRs.

- The guidelines provide a **full explanation of each level** and examples.  
- See `guidelines/ARCC_annotation_guidelines.pdf` for the complete annotation scheme.

---

## Corpus Structure

The anonymized version included in this repository (`corpus/ARCC_anonymized.csv`) contains the following fields:

| Column             | Description |
|--------------------|-------------|
| `Index`            | Row index |
| `subreddit`        | Subreddit name |
| `num_comments`     | Number of comments in the conversation |
| `speaker_id`       | Anonymized user ID |
| `conversation_id`  | ID of the conversation |
| `comment_id`       | Reddit comment/submission ID |
| `reply_to_comment` | Comment ID this is replying to |
| `segment_id`       | ID of the segment |
| `reply_to_segment` | Segment ID this segment replies to |
| `target_comment_id`| Comment ID targeted by this segment |
| `depth`            | Depth in the conversation tree |
| `segment_start`    | Character offset start of the segment |
| `segment_end`      | Character offset end of the segment |
| `SA`               | Speech Act label |
| `SUB-SA`           | Subjectivity label (5-degree scale) |
| `FDR`              | Functional Dependence Relation |
| `RR_intra`         | Intra-segment rhetorical relation (pilot) |
| `parent_SA`        | Parent segment’s speech act |
| `Biased`           | Biased marker (for biased questions) |


> **Note:** The corpus does **not include original comment text**. To reconstruct text, users must provide their own Reddit API credentials.

---

## Reconstruction of Text Segments

To reconstruct the actual text of the segments:

1. Fill in your own Reddit API credentials in `reconstruct_corpus.py`:

```python
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
