from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/rostom132/prefect_demo_user.git",
        entrypoint="flow.py:user_pipeline",
    ).deploy(
        name="user-pipeline-image-deployment", 
        work_pool_name="intern_demo",
        job_variables={
            "env": {
                "EXTRA_PIP_PACKAGES": "scikit-learn, psycopg2-binary",
                "HOST_POSTGREES": '0.tcp.ap.ngrok.io',
                "PORT_POSTGREES": 12693
            }
        },
    )