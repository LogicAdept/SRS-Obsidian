<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Deployment #SRS

# What is the service per VM pattern

> [!abstract] Short answer
> Service per VM: package each service as a virtual machine image (an AMI on AWS, a VMDK elsewhere) and run every service instance as its own VM. The deployment pattern - the classic Netflix example, which bakes each service into an EC2 AMI and autoscales EC2 instances - offers strong isolation and uniform operations at the price of slow builds and heavyweight resource usage.

## Mechanism: the image is the deployment unit

The service is baked into a machine image: OS, runtime, application - immutable and versioned. Deploying a new instance means launching that image; scaling means launching more copies behind a load balancer (AWS autoscaling groups can drive this on load); rolling back means launching the previous image. Every instance starts identical - configuration drift between servers, the classic operational disease of hand-maintained hosts, disappears. The VM boundary also normalizes operations: all services start and stop the same way regardless of their internal stack, instances are isolated from one another, and the VM caps CPU and memory per instance. The IaaS layer contributes mature machinery - load balancers, autoscaling groups, instance health checks - that the deployment story inherits rather than builds. On the ownership spectrum of the deployment patterns this is the heavyweight end: it refines single-service-per-host by making the host disposable, and it contrasts with container and serverless options ([[What is the service per container pattern]] is the modern default; [[What is the difference between Docker containers and virtual machines]] is the technology-level comparison).

```d2
direction: right
img: "Service VM image
OS + runtime + service v42" {style.fill: "#e8f5e9"}
lb: "Load balancer" {style.fill: "#eceff1"}
vm1: "VM instance 1" {style.fill: "#e8f5e9"}
vm2: "VM instance 2" {style.fill: "#e8f5e9"}
vm3: "VM instance 3" {style.fill: "#e8f5e9"}
asg: "Autoscaling group" {style.fill: "#fff3e0"}
img -> vm1: launch
img -> vm2: launch
img -> vm3: launch
asg -> vm1
asg -> vm2
asg -> vm3
lb -> vm1: traffic
lb -> vm2: traffic
lb -> vm3: traffic
```

**Fig. 1.** One immutable image fans out into identical instances; the autoscaling group and load balancer are inherited IaaS machinery.

## Where it stands today

The costs: building a VM image is slow and time-consuming - minutes of provisioning and boot per instance versus milliseconds-to-seconds for a container start; VMs carry a full guest OS each, so density and cost per service instance are poor; and slow spin-up blunts the elasticity that autoscaling is supposed to provide. The pattern remains legitimate where its strengths dominate: regulated environments demanding hypervisor-grade isolation between tenants or services, polyglot estates where one standard VM image format serves JVM, Go and Python services alike, and platforms already built around machine images (the Netflix history is exactly that). For most greenfield microservice deployments the same properties - immutability, isolation, horizontal scale - arrive cheaper through containers orchestrated by Kubernetes, with VMs remaining below as the substrate the containers run on. The interview-shaped framing: know service-per-VM as the pattern that established immutable machine images as deployment units; recognize that containers inherited that idea and shrank the unit.

> [!warning] Immutable does not mean current
> Baking images is only as good as the pipeline that rebuilds them: an image that was immutable in 2023 but never rebuilt carries stale OS packages and an unpatched OpenSSL forever. The discipline is rebuild-on-every-change, including OS patches - image provenance matters as much as application version. Second trap: instance-specific state on the VM's disk; the moment an instance writes meaningful local state, "launch another copy" stops being equivalent and horizontal scaling quietly breaks - state belongs in external stores.

> [!tip] Interview answer
> Service per VM packages each service as a machine image and runs every instance as its own VM - Netflix's AMI model. You get real isolation, uniform start/stop across stacks, autoscaling from IaaS, and zero config drift, at the cost of slow image builds, heavy resource footprint and slow scaling. Today containers usually deliver the same immutability cheaper, so I treat VM-per-service as the pattern for strong-isolation and legacy-IaaS contexts.
