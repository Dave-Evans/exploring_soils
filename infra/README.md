# Infrastructure

This README serves to document to myself what it is that I have learned about Terraform and Ansible, how I have used them in this project, and how I might use them in the future.
I am using Terraform to construct the AWS resources I'm using and using Ansible to manage and provision the servers.
I am not currently using anything specific to tie these two systems together, at the moment all configuration files are created and populated manually.

## Terraform

Terraform is an infrastructure as code software which allows us to create resources in the cloud in a reusable, code-based way.
Terraform uses a decrlaritive language, whereby we write up a list of what we want created in the cloud, and Terraform creates it.

The project in question is a very simple one and so the Terraform code necessary is not much.
Did we have to use Terraform here? No, but I wanted the chance to try to get more familiar.
The infrastructure consists of a single EC2 instance and S3 bucket, and an instance profile that allows the instance to access the bucket.

I have yet to build in the elastic ip address and I would also like to add at "Do not destroy" to the S3 bucket.
I would like to better understand what it would look like to build this out for a multi machine setup. 
In a situation where there are two webservers, a load balancers and a database server, how is the networking configured?

### References

[This](https://www.youtube.com/watch?v=UleogrJkZn0) was a helpful example.
I haven't yet explored [this](https://github.com/28mm/awesome-terraform) but it seems to be a comprehensive list of resources.
Multiple server configuration [here](https://medium.com/@dhelios/terraform-by-examples-part-1-ef3e3be7b88b)
Useful for variable defintion and SSL certs [here](https://medium.com/modern-stack/5-minute-static-ssl-website-in-aws-with-terraform-76819a12d412)

## Ansible

Ansible is a provisioning and configuration management software.
I am using this to do all the setup on the server. 
Since I'm on a single machine I could just use bash scripts and nest them inside a `remote-exec` tag in Terraform, but that seemed too boring.

I have setup the Ansible playbooks as if there is a database server as well as a web server, though its all on one for now. 
There are clever ways to have everything run through roles and so things can be executed with a single Ansible call, but I have not done that.
Right now, the db play must be run before the website because the website loads data to the database.
In the case where there are multiple webservers, there are several steps that would only need to be run on one of them.

A major todo I have is to manage the config files for Terraform and Ansible as well as for the Django project itself.
I think I may use `bash` for this but perhaps there is an easier and tidier solution somehwere.
Currently, I need to manually replace the web server's ip address and put it in the hosts file for Ansible as well as the `.env` file for the Django project. 
Similarly, the bucket name, AWS id and AWS secret key are in the `.env` file, the Terraform configs and the Ansible configs; something that needs tidying.

I need to look into Dynamic inventory.

### How to run

These ansible files require a file at `./ansible/vars/main.yml` which would look like this:
```yaml
---
db_user: db_user_name
db_name: database_name
db_password: mycoolpassword
```

It also requires `./ansible/hosts` file, looking like:
`12.345.678.910 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/sandbox1.pem`

Querying output variables
`ssh -i ~/.ssh/sandbox1.pem ubuntu@$(terraform output ip)`
`ssh -i ~/.ssh/sandbox1.pem ubuntu@$(terraform output el_pub_ip)`


`aws s3 cp ./test.txt s3://greencover-sandbox/test.txt`


### References

 - https://www.youtube.com/watch?v=UleogrJkZn0
 - [Cron job](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/cron_module.html)
 - [For Django and Ansible](https://realpython.com/automating-django-deployments-with-fabric-and-ansible/)
 - [Ansible loop](https://linuxhint.com/install_multiple_packages_centos_ansible/)
 - [Ansible examples](https://github.com/ansible/ansible-examples/tree/master/lamp_simple)
 - [Here](https://ansible.github.io/workshops/exercises/ansible_rhel/1.2-adhoc/) 
 - What the hell is `become`? [Check here](http://docs.ansible.com/ansible/latest/user_guide/become.html)


```sh
# Added community with 
# ansible-galaxy collection install community.general
echo "$(terraform output el_pub_ip) ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/sandbox1.pem" > hosts

ansible-playbook -i hosts database.yml
# must be run after db is setup
ansible-playbook -i hosts website.yml
ansible-playbook -i hosts update.yml
```

