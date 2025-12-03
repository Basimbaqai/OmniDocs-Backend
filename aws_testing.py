from aws_config import s3_client, S3_BUCKET_NAME
import io


def test_s3_connection():
    try:
        # Try to upload a test file
        test_content = b"Hello S3!"
        test_file = io.BytesIO(test_content)

        s3_client.upload_fileobj(test_file, S3_BUCKET_NAME, "test/test.txt")
        print("✅ Successfully uploaded test file to S3!")

        # Clean up
        s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key="test/test.txt")
        print("✅ S3 connection test passed!")

    except Exception as e:
        print(f"❌ S3 test failed: {e}")


if __name__ == "__main__":
    test_s3_connection()
