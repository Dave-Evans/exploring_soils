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

### Protecting resources

It seems there is no great method in Terraform for protecting resources from destruction.
It's possible to add a lifecycle tag and use `prevent_destroy` or some such, but this just throws an error when tearing down.
I would like to have the S3 bucket and the Elastic IP kept from being destroyed. 
The S3 bucket will have content in it and so it won't be deleted.
But the IP address will. 
My thinking is that for all non-production uses of this code, no elastic ip address will be used; it will be skipped.
However, for prod use, I will merely attach the elastic IP address, which I will just have created manually.
Considerations:
I will need an if statements in the Terraform code, if prod (in variables?) then use IP address, if not then forget it.
I am going to leave this undone for now and proceed with assuming that we aren't going to use an elastic ip.

### References

[For booleans](https://blog.gruntwork.io/terraform-tips-tricks-loops-if-statements-and-gotchas-f739bbae55f9)
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
database_user: db_user_name
database_name: database_name
database_pass: mycoolpassword
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


## Workflow

The bash script `helper.sh` is used to run Terraform and Ansible within one program.
It allows us maintain only one config file, the `.env` file, which is used by `decouple` within the Django application.
See the example file `.env.example` for what this should look like.
If you aren't going to use the default named environment file, `.env`, then specify the path to your env file with `-f ../test.env`.
The helper program first generates the Terraform and Ansible variable files using
`./helper.sh create_vars`.
Then, it calls the Terraform code, `./helper.sh spinup_infra`.
After this, provision and configure the infrastructure with Ansible using `./helper.sh deploy`.
