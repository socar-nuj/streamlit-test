import uvicorn


def run_server():
    uvicorn.run("somlier.external_interfaces.container:create_app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run_server()
