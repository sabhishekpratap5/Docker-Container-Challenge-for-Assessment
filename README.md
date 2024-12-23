# Docker-Container-Challenge-for-Assessment
**Section 1: 
**
**Resolution Steps
**
1. Analyze Logs
   - Checked the logs after running the provided image.
   - Found the error:
     2024/12/23 17:15:00 [emerg] 10#10: open() "/etc/nginx/nginxo2.conf" failed (2: No such file or directory)
   - Identified a typo in the file name `nginxo2.conf`, which should be `nginx02.conf`.

2. Fix Entrypoint Configuration
   - Inspected the `entrypoint.sh` file and corrected the reference to `nginxo2.conf` to `nginx02.conf`.
   - Reloaded the NGINX configuration using:
     nginx -s reload

3. Update HAProxy Configuration
   - Located the HAProxy configuration file at `/usr/local/etc/haproxy/haproxy.cfg`.
   - Found that HAProxy was incorrectly set to use ports `8000`, `8001`, and `8003` for the backend servers.
   - Updated the configuration to use the correct ports:
     backend webservers
         mode http
         server localhost-01 localhost:8001
         server localhost-02 localhost:8002
         server localhost-03 localhost:8003

4. Restart HAProxy
   - Restarted HAProxy to apply the updated configuration:
     haproxy -f /usr/local/etc/haproxy/haproxy.cfg

5. Validate the Fix
   - Verified that HAProxy was successfully load-balancing traffic across all three NGINX servers.

6. Save and Push the Fixed Image
   - Committed the corrected container with the name `aps123/docker-challenge`.
   - Pushed the updated image to Docker Hub:
     docker commit <container_id> aps123/docker-challenge
     docker push aps123/docker-challenge

7. Run the Fixed Image
   - Provided the following command to run the updated image:
     docker run -d   --name haproxy_container   -p 80:80   aps123/docker-challenge

Outcome
- The issue was resolved successfully.
- HAProxy now correctly load-balances traffic across the NGINX servers on ports `8001`, `8002`, and `8003`.


**Section2: 
**


# Steps to Run the Ansible Playbook and Docker Image

This document provides the steps to execute the Ansible playbook and run the Docker images for HAProxy and Metrics Scraper.

---

## Prerequisites
1. **Ensure Docker is Installed**:
   If Docker is not already installed, install it using:
   ```bash
   sudo apt update
   sudo apt install docker.io -y
   ```

2. **Ensure Ansible is Installed**:
   If Ansible is not already installed, install it using:
   ```bash
   sudo apt update
   sudo apt install ansible -y
   ```

3. **Ensure Docker Hub Account**:
   Make sure you have a Docker Hub account for pushing images. You will need the image names for HAProxy and Metrics Scraper.

---

## Step 1: Set Up Project Directory

1. **Create the project directory**:
   ```bash
   mkdir haproxy_ansible
   cd haproxy_ansible
   ```

2. **Create the directory structure**:
   ```plaintext
   haproxy_ansible/
   ├── playbook.yml
   ├── roles/
   │   ├── haproxy/
   │   │   ├── tasks/
   │   │   │   └── main.yml
   │   ├── metrics_scraper/
   │   │   ├── tasks/
   │   │   │   └── main.yml
   ├── app.py       # Metrics scraper application
   └── Dockerfile   # Dockerfile for the scraper
   ```

---

## Step 2: Create Ansible Playbook and Roles

1. **Create the `playbook.yml`**:
   - This playbook will call both the HAProxy and Metrics Scraper roles.
   ```yaml
   ---
   - hosts: localhost
     become: yes
     tasks:
       - name: Include HAProxy role
         include_role:
           name: haproxy

       - name: Include Metrics Scraper role
         include_role:
           name: metrics_scraper
   ```

2. **Create HAProxy Role** (`roles/haproxy/tasks/main.yml`):
   - Manages the HAProxy container:
   ```yaml
   ---
   - name: Ensure Docker is installed
     apt:
       name: docker.io
       state: present

   - name: Start Docker service
     service:
       name: docker
       state: started
       enabled: yes

   - name: Pull HAProxy container image
     docker_image:
       name: your_docker_hub/haproxy_fixed
       tag: latest
       source: pull

   - name: Run HAProxy container
     docker_container:
       name: haproxy
       image: your_docker_hub/haproxy_fixed:latest
       ports:
         - "80:80"
       state: started
   ```

3. **Create Metrics Scraper Role** (`roles/metrics_scraper/tasks/main.yml`):
   - Manages the Metrics Scraper container:
   ```yaml
   ---
   - name: Pull Metrics Scraper container image
     docker_image:
       name: your_docker_hub/metrics_scraper
       tag: latest
       source: pull

   - name: Run Metrics Scraper container
     docker_container:
       name: metrics_scraper
       image: your_docker_hub/metrics_scraper:latest
       ports:
         - "8080:8080"
       state: started
   ```

---

## Step 3: Build and Push Docker Images (If Needed)

1. **Build the Metrics Scraper Image** (if not already built):
   - Navigate to the directory where `app.py` and `Dockerfile` are located.
   ```bash
   docker build -t your_docker_hub/metrics_scraper .
   ```

2. **Push the Metrics Scraper Image**:
   - Push the Docker image to Docker Hub.
   ```bash
   docker push your_docker_hub/metrics_scraper
   ```

3. **Push the Fixed HAProxy Image** (if not already done):
   - After fixing the HAProxy container, push it to Docker Hub:
   ```bash
   docker commit <container_id> your_docker_hub/haproxy_fixed:latest
   docker push your_docker_hub/haproxy_fixed:latest
   ```

---

## Step 4: Run the Ansible Playbook

1. **Execute the Ansible Playbook**:
   - Run the playbook to deploy the containers:
   ```bash
   ansible-playbook playbook.yml
   ```

   This will:
   - Install Docker (if not installed).
   - Pull the Docker images for HAProxy and Metrics Scraper.
   - Start the HAProxy container on port `80` and the Metrics Scraper container on port `8080`.

---

## Step 5: Verify the Containers

1. **Verify HAProxy**:
   - Open a browser or use `curl` to check if HAProxy is running:
   ```bash
   curl http://localhost
   ```
   HAProxy should load-balance traffic to the Metrics Scraper container.

2. **Verify Metrics Scraper**:
   - Check if the Metrics Scraper API is available:
   ```bash
   curl http://localhost:8080/metrics
   ```
   You should see JSON output with system metrics like CPU and memory usage.



---

## Conclusion

By following these steps, you have:
1. Built and deployed HAProxy and Metrics Scraper containers using Ansible.
2. Verified that the HAProxy container is load-balancing traffic and the Metrics Scraper container is exposing system metrics.

---
