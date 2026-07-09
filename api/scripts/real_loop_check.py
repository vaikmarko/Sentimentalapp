"""Manual end-to-end check of the core loop against REAL providers.

Usage: python3 scripts/real_loop_check.py  (reads OPENAI_API_KEY from api/.env)
Costs a few cents. Not part of the test suite.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.auth import AuthedUser, get_current_user  # noqa: E402
from app.main import app  # noqa: E402

SAMPLE_ET = (
    "Ma käisin eile õhtul vanaema juures. Ta elab ikka veel selles samas "
    "korteris Mustamäel, kus ma lapsena suvesid veetsin. Ta tegi pannkooke "
    "ja ütles, et ma olen liiga kõhnaks jäänud, nagu alati. Köögis lõhnas "
    "täpselt samamoodi nagu kakskümmend aastat tagasi. Mingi hetk ta hakkas "
    "rääkima vanaisast, kuidas nad nooruses Pärnu rannas käisid, ja ta "
    "naeris nii, et pisarad tulid silma. Ma ei osanud midagi öelda, "
    "istusin lihtsalt ja kuulasin. Koju sõites mõtlesin, et peaksin "
    "tihedamini käima. Iga kord ma mõtlen seda."
)


def main() -> None:
    app.dependency_overrides[get_current_user] = lambda: AuthedUser(
        uid="founder-real-test", email="founder@test", name="Founder"
    )
    client = TestClient(app)

    print("Posting Estonian text entry against REAL providers...")
    res = client.post("/api/entries/text", json={"text": SAMPLE_ET})
    res.raise_for_status()
    entry_id = res.json()["entry_id"]

    result = client.get(f"/api/entries/{entry_id}").json()
    print(f"\nStatus: {result['status']}")
    story = result.get("story")
    if not story:
        print("No story produced — check pipeline logs above.")
        sys.exit(1)

    print(f"\n=== {story['title']} ===")
    print(story["story"])
    print(f"\nLanguage: {story['language']}")
    print(f"Signature: {story['signature']}")
    print(f"Recommendation: {story['recommendation']}")
    print(f"Support flag: {story['support_flag']}")


if __name__ == "__main__":
    main()
