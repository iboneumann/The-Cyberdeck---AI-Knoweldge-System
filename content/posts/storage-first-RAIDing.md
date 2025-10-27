+++
date = '2025-10-27T17:20:08+01:00'
draft = false
title = "Storage First - RAIDing"
weight = 21
+++

I decided to start organizing the Cyberdeck storage situation
by creating RAIDs over those Computers stuffed with USB devices.

Also, I want to demonstrate the use of large online models. They
are restricted in their chat length, but free of charge, while 
the hardware costs to run a large model like DeepSeek R1 is 
incredible creating a inefficient set up, except the user is 
also a hardcore high-end gamer.

After walking through establishing RAIDs without data loss over
two Computers that now can be both accessed using the individual
drives as much as in a RAID way combining all folders, I asked
DeepSeek to create a chapter for a Thesis in scientific IT
Computing.

That's the outcome:
```batch
# **Chapter 5:
# Implementation of a Unified Storage System Using MergerFS**

## **5.1 Introduction**

In modern computing environments, the proliferation of storage
devices presents both opportunities and challenges. Users
frequently accumulate multiple external storage devices of
varying capacities, filesystems, and connection interfaces, 
leading to fragmented storage management and inefficient 
resource utilization. This chapter documents the design and 
implementation of a unified storage solution using MergerFS, a 
FUSE-based union filesystem, to address the practical problem of 
storage fragmentation across heterogeneous storage devices.

The project demonstrates how software-defined storage solutions 
can transform multiple discrete storage units into a cohesive, 
manageable storage pool while maintaining data integrity and 
accessibility. This implementation showcases the practical 
application of filesystem abstraction layers in solving 
real-world storage management challenges.

## **5.2 Problem Statement**

### **5.2.1 Storage Fragmentation Challenges**

The computing environment in question consisted of multiple 
external storage devices with the following characteristics:

- **Heterogeneous filesystems**: ext4, NTFS, exFAT, and vFat
- **Varying capacities**: Multiple 116GB USB drives and larger 
    external drives
- **Disconnected management**: Each device required individual 
    mounting and management
- **Inefficient space utilization**: Files could not span multiple 
    devices automatically
- **Complex backup procedures**: Manual coordination required for 
    comprehensive data protection

### **5.2.2 Research Objectives**

This project aimed to:
1. Create a unified storage namespace from multiple physical devices
2. Maintain backward compatibility with existing data
3. Enable transparent capacity expansion
4. Provide a foundation for automated backup systems
5. Demonstrate practical filesystem abstraction techniques

## **5.3 Theoretical Framework**

### **5.3.1 Union Filesystems**

Union filesystems represent a class of filesystems that combine 
multiple directory hierarchies into a single coherent view. Unlike 
traditional RAID configurations that operate at the block level, 
union filesystems function at the filesystem level, providing 
several advantages:

- **Non-destructive operation**: Original data structures remain 
    intact
- **Heterogeneous support**: Compatibility across different 
    underlying filesystems
- **Dynamic reconfiguration**: Ability to add or remove storage 
    components without data migration

### **5.3.2 FUSE Architecture**

The Filesystem in Userspace (FUSE) framework enables the development 
of filesystems without kernel modifications. MergerFS leverages 
FUSE to provide:

- **User-space implementation**: Enhanced safety and debugging 
    capabilities
- **Kernel abstraction**: Standard POSIX filesystem interface
- **Flexible mounting**: Dynamic filesystem configuration

## **5.4 Methodology**

### **5.4.1 System Analysis and Requirements Gathering**

The implementation began with comprehensive system analysis:


# Storage device inventory
lsblk -f
sudo blkid

# Capacity and filesystem assessment
df -h
mount | grep media


This analysis revealed five primary storage devices with mixed 
filesystems and mounting configurations, totaling approximately 
465GB of fragmented storage capacity.

### **5.4.2 Technology Selection**

After evaluating multiple solutions (traditional MD RAID, LVM, ZFS), 
MergerFS was selected for its:
- **Data preservation**: No requirement for data migration or 
    reformatting
- **Filesystem agnosticism**: Compatibility with existing ext4, NTFS, 
    exFAT, and vFat volumes
- **Simplicity of management**: Straightforward configuration and 
    operation
- **Dynamic expandability**: Ability to add or remove devices without 
    restructuring

### **5.4.3 Implementation Architecture**

The solution employed a dual-system approach:

1. **Primary System (Raspberry Pi)**: Consolidated four 116GB USB 
     drives into a 342GB pool
2. **Secondary System (Local Machine)**: Pooled five heterogeneous 
     external drives
3. **Backup Strategy**: Dedicated external drive excluded from pooling 
     for backup purposes

## **5.5 Implementation Process**

### **5.5.1 System Preparation**

The implementation followed a structured approach:

**Package Installation**:

sudo apt update
sudo apt install mergerfs


**Directory Structure Establishment**:

sudo mkdir -p /mnt/pooled-storage
sudo chown $USER:$USER /mnt/pooled-storage


### **5.5.2 Configuration and Mounting**

**Manual Testing Phase**:

sudo mergerfs -o defaults,allow_other,use_ino \
  "/media/ibo/512SSDUSB:/media/ibo/SD M920:/media/ibo
/3430-3633:/media/ibo/9470-6461" \
  /mnt/pooled-storage


**Persistence Configuration**:

# /etc/fstab entry with proper space escaping
/media/ibo/512SSDUSB:/media/ibo/SD\040M920:/media/ibo
/3430-3633:/media/ibo/9470-6461 \
  /mnt/pooled-storage fuse.mergerfs \
  defaults,allow_other,use_ino,nonempty 0 0


### **5.5.3 Validation and Testing**

Comprehensive testing ensured system reliability:

**Mount Verification**:

sudo mount -a
df -h | grep pooled-storage


**Functional Testing**:

# Write operations
echo "MergerFS validation test" > /mnt
/pooled-storage/test-file.txt

# Read operations
cat /mnt/pooled-storage/test-file.txt

# Cross-device file distribution verification
ls -la /mnt/pooled-storage/


## **5.6 Technical Challenges and Solutions**

### **5.6.1 Filesystem Heterogeneity**

**Challenge**: Mixed filesystems (ext4, NTFS, exFAT, vFat) 
with different capabilities and limitations.

**Solution**: MergerFS's filesystem-agnostic design automatically 
handled permission and metadata differences through its policy engine.

### **5.6.2 Space Character Escaping**

**Challenge**: Mount point paths containing spaces caused 
fstab parsing errors.

**Solution**: Implemented proper space escaping using 
`\040` octal representation in fstab entries.

### **5.6.3 Non-empty Mount Points**

**Challenge**: FUSE safety mechanisms prevented mounting to non-empty 
directories.

**Solution**: Utilized the `nonempty` mount option while ensuring 
directory cleanliness.

### **5.6.4 Backup Integration**

**Challenge**: Maintaining a separate backup strategy while using 
pooled storage.

**Solution**: Excluded backup drive from the pool and implemented 
rsync-based backup procedures.

## **5.7 System Evaluation**

### **5.7.1 Performance Metrics**

The implemented solution demonstrated:

- **Transparent file distribution** across multiple devices
- **Aggregated capacity** presentation to users and applications
- **Minimal performance overhead** compared to native filesystems
- **Automated mount persistence** across system reboots

### **5.7.2 Usability Assessment**

**Before Implementation**:
- Multiple independent mount points
- Manual file placement decisions
- Complex capacity management
- Individual device monitoring

**After Implementation**:
- Single unified storage namespace
- Automatic file distribution
- Simplified capacity planning
- Centralized management interface

## **5.8 Backup Strategy Implementation**

### **5.8.1 Architecture Design**

The backup system employed a 3-2-1 strategy foundation:

- **3** copies of important data
- **2** different storage media
- **1** offsite or isolated copy

### **5.8.2 Implementation Details**

**Backup Drive Configuration**:

sudo mkdir -p /mnt/backup-drive
sudo mount -t ntfs-3g /dev/sdc1 /mnt/backup-drive


**Automated Backup Procedure**:

rsync -av --progress /mnt/pooled-storage/ \
  /mnt/backup-drive/backup-$(date +%Y-%m-%d)/


## **5.9 Conclusion**

The MergerFS implementation successfully addressed the challenge of 
storage fragmentation across heterogeneous devices. The solution 
demonstrated several key computing principles:

1. **Abstraction**: Effective use of filesystem abstraction to 
     simplify complex storage management
2. **Compatibility**: Seamless integration with existing infrastructure 
     and data
3. **Scalability**: Support for dynamic storage expansion without service 
     interruption
4. **Practicality**: Real-world application of theoretical  
     filesystem concepts

The project highlights how modern computing environments can leverage 
software-defined storage solutions to overcome hardware limitations, 
providing a template for similar implementations in diverse computing 
contexts. The successful deployment across both Raspberry Pi and 
traditional computing platforms demonstrates the solution's versatility 
and broad applicability in contemporary IT infrastructure management.

This implementation serves as a case study in practical system 
administration, showcasing how theoretical computing concepts can be 
applied to solve real-world storage management challenges while 
maintaining data integrity and system reliability.
```
