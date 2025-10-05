from dynatrace_fastlane import DynatraceFastlaneUploader

uploader = DynatraceFastlaneUploader(project_dir="/path/to/ios/project")

uploader.process_symbols(
    app_id="eab451f3-5208-4c52-b06a-df09f86c2cb3",
    api_token="dt0c01.ABCDEF1234567890",
    dtx_client_path="./DTXDssClient",
    symbol_file="./MyApp.app.dSYM.zip",
    bundle_name="com.mycompany.myapp",
    version_str="1.0.0",
    version="100",
    server_url="https://yourtenant.live.dynatrace.com/e/abc123",
    debug_mode=True
)