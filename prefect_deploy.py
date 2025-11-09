from datetime import timedelta
from prefect_flow import pipeline  


if __name__ == "__main__":
    pipeline.serve(name = "Weekly NBA Update",
                   tags = ["onboarding"],
                   interval = 60 * 60 * 24 * 7)