// import S3 from '@aws-sdk/client-s3';
import {S3Client,PutObjectCommand} from '@aws-sdk/client-s3';
import { readFileSync } from 'fs';
console.log(process.env.AWS_REGION)
const s3 = new S3Client({
    credentials : {
        accessKeyId: `${process.env.AWS_ACCESS_KEY_ID}`,
        secretAccessKey: `${process.env.AWS_SECRET_ACCESS_KEY}`
    },
   })


const file_upload = async (filePath, bucket, fileName) => {
    try {
        const file_content = readFileSync(filePath, 'utf-8');
        const input  = {
            "Body" : `${file_content}`,
            "Bucket" : `${bucket}`,
            "Key" : `${fileName}`,
        }
        const command  = new PutObjectCommand(input);
        const response = await s3.send(command);
        console.log(response);
    } catch (err) {
        console.error('Error uploading file to S3:', err);
    }
}

const file = './output.txt';
const fileName = 'output.txt';
const bucket = process.env.BUCKET_NAME;
file_upload(file, bucket, fileName);
