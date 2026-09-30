from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.database import Base, engine

from app.models import driver as driver_model
from app.models import truck as truck_model
from app.models import load as load_model
from app.models import expense as expense_model

from app.routes import driver
from app.routes import truck
from app.routes import load
from app.routes import expense


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Dispatch OS API",
    version="1.0.0",
    description="Left Door Shut Dispatch management platform API",
    docs_url=None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(driver.router)
app.include_router(truck.router)
app.include_router(load.router)
app.include_router(expense.router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    html = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
    )

    content = html.body.decode("utf-8")

    custom_css = """
    <style>
        .opblock-summary-method {
            width: auto !important;
            min-width: 110px !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
            text-align: center !important;
        }

        .opblock-summary-description {
            display: none !important;
        }
    </style>
    """

    custom_script = """
    <script>
        (function () {
            let observer = null;
            let scheduled = false;

            function renameSwaggerMethods() {
                if (observer) {
                    observer.disconnect();
                }

                document.querySelectorAll(".opblock-summary").forEach(function (summary) {
                    const method = summary.querySelector(".opblock-summary-method");
                    const description = summary.querySelector(".opblock-summary-description");

                    if (!method || !description) {
                        return;
                    }

                    const title = description.textContent.trim();

                    if (title && method.textContent.trim() !== title) {
                        method.textContent = title;
                    }
                });

                if (observer) {
                    observer.observe(document.body, {
                        childList: true,
                        subtree: true
                    });
                }
            }

            function scheduleRename() {
                if (scheduled) {
                    return;
                }

                scheduled = true;

                requestAnimationFrame(function () {
                    scheduled = false;
                    renameSwaggerMethods();
                });
            }

            window.addEventListener("load", function () {
                setTimeout(renameSwaggerMethods, 300);
                setTimeout(renameSwaggerMethods, 1000);
                setTimeout(renameSwaggerMethods, 2000);

                observer = new MutationObserver(function () {
                    scheduleRename();
                });

                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });
            });
        })();
    </script>
    """

    content = content.replace("</head>", custom_css + "</head>")
    content = content.replace("</body>", custom_script + "</body>")

    return HTMLResponse(content=content)


@app.get("/")
def read_root():
    return {
        "message": "Dispatch OS API running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "dispatch-os-api",
        "version": "1.0.0",
    }
