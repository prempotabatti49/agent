------------------------------------------------------
## 🐳 Run and Stop the Docker Image Locally
### 🔧 Build and Run the Docker Image
In the project folder, run:

```bash
docker build -t my-fastapi-app .
docker run -p 8080:8080 my-fastapi-app
```

## Access the app:
http://localhost:8080/docs

## Stop the docker container:
```
docker ps --> get the image ID (abc123def456)
docker stop abc123def456
```
------------------------------------------------------

# AWS Deployment
1️⃣ Create ECR Repository

Go to ECR (Elastic Container Registry) in AWS console.


Click “Create Repository”.

Name it my-fastapi-app.

After creating, note down the repository URI (like 523473407569.dkr.ecr.us-east-1.amazonaws.com/my-fastapi-app).



2️⃣ Push Docker image to ECR

In your terminal:
```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 523473407569.dkr.ecr.us-east-1.amazonaws.com
(gets temporary token from aws and puts into the docker login command using --password-stdin)

docker tag my-fastapi-app:latest 523473407569.dkr.ecr.us-east-1.amazonaws.com/my-fastapi-app:latest
(This command is used to tag a Docker image so it can be pushed to a specific Amazon Elastic Container Registry (ECR) repository)

docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-fastapi-app:latest
(This command is used to upload a Docker image from your local machine to your Amazon Elastic Container Registry (ECR))
```

3️⃣ Create ECS Cluster

Go to ECS → “Create Cluster”.

Choose “Networking only (Fargate)”.

Give it a name, e.g. fastapi-cluster.

4️⃣ Create Task Definition

Go to “Task Definitions” → “Create new task definition”.

Choose Fargate.

Add container:

Name: fastapi-container

Image URI: (paste your ECR image URI)

Port mappings: 8080

CPU: 0.25 vCPU, Memory: 0.5GB

Add Environment variables:

e.g., OPENAI_API_KEY, loaded from your .env

5️⃣ Create Service

Go to your ECS Cluster → “Create Service”.

Choose Fargate.

Attach the Task Definition.

Number of tasks: 1.

In Networking, attach a VPC + Subnet + Security group (allow inbound 8080).

Enable a Public Load Balancer if you want public access.

After it runs, ECS will show a public endpoint or load balancer URL.

✅ That’s your deployed API URL!

🌐 STEP 6 — Calling the API from Web or Postman

Let’s say your deployed URL is:
http://fastapi-1234567890.us-east-1.elb.amazonaws.com/chat

curl -X POST http://fastapi-1234567890.us-east-1.elb.amazonaws.com/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"Hello there!"}'
