#!/usr/bin/env python3
import sys, getopt, os

class CodeFreeze_PList:
    className = "CodeFreeze_PList"
    className_string = "Code Freeze - PList"
    classPrefix = "Release List"

    import plistlib

    def __init__(self,DisplayMSG=False):
        self.FileName = "release.plist"
        self.Folder = ""

        self.Path = os.path.abspath(os.path.join(RepoRoot, self.Folder))
        self.FullName = os.path.abspath(os.path.join(self.Path, self.FileName))
        self.Validate = os.path.exists(self.FullName)

        self.Current_release_name = ""
        self.Current_release_version = ""

        self.Next_release_name = ""
        self.Next_release_version = ""

        self.ReadList()

    def DisplayClassInfo(self,DisplayMSG=False):
        print ("")
        print ("{} (Path): {}".format(self.classPrefix, self.Path))
        print ("{} (File Name): {}".format(self.classPrefix, self.FileName))
        print ("{} (Full Name): {}".format(self.classPrefix, self.FullName))
        print ("{} (Validate): {}".format(self.classPrefix, self.Validate))
        print ("")
        print ("Current Release (Name): {}".format(self.Current_release_name))
        print ("Current Release (Version): {}".format(self.Current_release_version))
        print ("")
        print ("Next Release (Name): {}".format(self.Next_release_name))
        print ("Next Release (Version): {}".format(self.Next_release_version))

    def ReadList(self,DisplayMSG=False):
        try:
            with open(self.FullName, 'rb') as fp:
                p = self.plistlib.load(fp)

            self.Current_release_name = p["SLKReleaseName"]
            self.Current_release_version = p["CFBundleShortVersionString"]

        except:
            print("Error: Reading plist ({})".format(self.FullName))

    def WriteList(self,DisplayMSG=False):
        print ("Updating PList with next release information:")

        try:
            with open(self.FullName, 'rb') as fp:
                p = self.plistlib.load(fp)

            if ((self.Next_release_name and self.Next_release_name.strip())):
                if not self.Next_release_name == self.Current_release_name:
                    print ("Update Release Name: \n\tCurrent: {}\n\tNext: {}".format(self.Current_release_name,self.Next_release_name))
                    p["SLKReleaseName"] = self.Next_release_name.strip()
                else:
                    print ("\tNext Release and Current Release match. Name: ({}/{})".format(self.Current_release_name,self.Next_release_name))
            else:
                print ("Next Release (Name) undefined.")

            if ((self.Next_release_version and self.Next_release_version.strip())):
                if not self.Next_release_version == self.Current_release_version:
                    print ("Update Release Version: \n\tCurrent: {}\n\tNext: {}".format(self.Current_release_version,self.Next_release_version))
                    p["CFBundleShortVersionString"] = self.Next_release_version.strip()
                else:
                    print ("\tNext Release and Current Release match. Version: ({}/{})".format(self.Current_release_version,self.Next_release_version))
            else:
                print ("Next Release (Version) undefined.")

            with open(self.FullName, 'wb') as fp:
                self.plistlib.dump(p, fp)
        except:
            print("Error: Write to plist ({})".format(self.FullName))

class CodeFreeze_ReleaseInfo:
    className = "CodeFreeze_ReleaseInfo"
    className_string = "Code Freeze - ReleaseInfo"
    classPrefix = "Release Info"

    import csv

    def __init__(self,DisplayMSG=False):
        self.FileName = "release_info.csv"
        self.Folder = "releng"

        self.Path = os.path.abspath(os.path.join(RepoRoot, self.Folder))
        self.FullName = os.path.abspath(os.path.join(self.Path, self.FileName))
        self.Validate = os.path.exists(self.FullName)

        self.ReleaseIndex = ""

        self.Previous_release_name = ""
        self.Previous_release_version = ""
        self.Previous_release_branch = ""
        
        self.Current_release_name = ""
        self.Current_release_version = ""
        self.Current_release_branch = ""

        self.Next_release_name = ""
        self.Next_release_version = ""
        self.Next_release_branch = ""

        self.ReadList()
        self.BranchStatusCheck()

    def DisplayClassInfo(self,DisplayMSG=False):
        print ("")
        print ("{} (Path): {}".format(self.classPrefix, self.Path))
        print ("{} (File Name): {}".format(self.classPrefix, self.FileName))
        print ("{} (Full Name): {}".format(self.classPrefix, self.FullName))
        print ("{} (Validate): {}".format(self.classPrefix, self.Validate))

        print ("Previous Release (Name): {}".format(self.Previous_release_name))
        print ("Previous Release (Version): {}".format(self.Previous_release_version))
        print ("Previous Release (Branch): {}".format(self.Previous_release_branch))
        
        print ("Current Release (Name): {}".format(self.Current_release_name))
        print ("Current Release (Version): {}".format(self.Current_release_version))
        print ("Current Release (Branch): {}".format(self.Current_release_branch))
        
        print ("Next Release (Name): {}".format(self.Next_release_name))
        print ("Next Release (Version): {}".format(self.Next_release_version))
        print ("Next Release (Branch): {}".format(self.Next_release_branch))

        for row in self.ReleaseIndex:
            print(row['rls_name'], row['rls_ver'])

    def ReadList(self,DisplayMSG=False):
        try:
            with open (self.FullName, newline='') as csvfile:
                CSVData = self.csv.DictReader(csvfile)
                self.ReleaseIndex = list(CSVData)
        except:
            print("Error: Reading list ({})".format(self.FullName))

    def BranchStatusCheck(self,DisplayMSG=False):
        MethodStatus = "EMPTY" # Create an empty variable for empty methoud to be used in the future.

    def ReleaseInformationData(self,DisplayMSG=False,CurrentVersion=0):
        i = 0
        PreviousReleaseID = 0
        CurrentReleaseID = 0
        NextReleaseID = 0
        MaxLen = len(self.ReleaseIndex)

        # print(MaxLen)

        for ProcessReleases in self.ReleaseIndex:
            if str(ProcessReleases['rls_ver']) == CurrentVersion:
                CurrentReleaseID = i
            i += 1

        # print("Index ID: {}".format(CurrentReleaseID))
        # print ("Index Point: {}".format(self.ReleaseIndex[CurrentReleaseID]['rls_ver']))

        PreviousReleaseID = CurrentReleaseID - 1
        NextReleaseID = CurrentReleaseID + 1
        
        self.Previous_release_name = self.ReleaseIndex[PreviousReleaseID]['rls_name']
        self.Previous_release_version = self.ReleaseIndex[PreviousReleaseID]['rls_ver']
        self.Previous_release_branch = ("{}/{}".format(self.ReleaseIndex[PreviousReleaseID]['rls_name'],self.ReleaseIndex[PreviousReleaseID]['rls_ver']))

        self.Current_release_name = self.ReleaseIndex[CurrentReleaseID]['rls_name']
        self.Current_release_version = self.ReleaseIndex[CurrentReleaseID]['rls_ver']
        self.Current_release_branch = ("{}/{}".format(self.ReleaseIndex[CurrentReleaseID]['rls_name'],self.ReleaseIndex[CurrentReleaseID]['rls_ver']))

        if NextReleaseID < MaxLen:
            self.Next_release_name = self.ReleaseIndex[NextReleaseID]['rls_name']
            self.Next_release_version = self.ReleaseIndex[NextReleaseID]['rls_ver']
            self.Next_release_branch = ("{}/{}".format(self.ReleaseIndex[NextReleaseID]['rls_name'],self.ReleaseIndex[NextReleaseID]['rls_ver']))
        else:
            print ("ERROR!! No more releases available.")

        print ("Previous Release: \t{} {} ({})".format(self.Previous_release_name, self.Previous_release_version, self.Previous_release_branch))
        print ("Current Release: \t{} {} ({})".format(self.Current_release_name, self.Current_release_version, self.Current_release_branch))
        print ("Next Release: \t\t{} {} ({})".format(self.Next_release_name, self.Next_release_version, self.Next_release_branch))


class CodeFreeze_GIT:
    className = "CodeFreeze_GIT"
    className_string = "Code Freeze - GIT"
    classPrefix = "GIT"

    import subprocess

    def __init__(self,DisplayMSG=False):
        self.BranchStatus = ""
        self.Previous_BranchName = ""
        self.Previous_BranchStatus = ""
        self.Current_BranchName = ""
        self.Current_BranchStatus = ""
        self.Release_BranchName = ""
        self.Release_BranchStatus = ""
        self.BranchList = ""

        self.CheckFile = ""
        self.Checkfile_Report = "Report.txt"

        global RepoRoot

        RepoRoot = os.path.abspath(os.path.join(ScriptRoot, ".."))
        self.RepoRoot_ValidateTest = os.path.abspath(os.path.join(RepoRoot, ".git"))
        self.RepoRoot_Validate = os.path.exists(self.RepoRoot_ValidateTest)

    def DisplayClassInfo(self,DisplayMSG=False):
        print ("")
        print ("Repo Root: {}".format(RepoRoot))
        print ("Repo Root (Validate Test): {}".format(self.RepoRoot_ValidateTest))
        print ("Repo Root (Validate): {}".format(self.RepoRoot_Validate))

        print("{} Branch Status: {}".format(self.classPrefix, self.BranchStatus))

    def DisplayClassInfo_Branchs(self,DisplayMSG=False):
        print(self.BranchListRAW.stdout)
        print(self.BranchListRAW.stderr)

        for row in self.BranchList:
            print (row)

    def CheckBranch(self,DisplayMSG=False):
        cmd = "git branch -a"
        self.BranchListRAW = self.subprocess.run(cmd, shell=True, capture_output=True)

        self.BranchList = self.BranchListRAW.stdout.splitlines()

        #--- Current Branch
        CurrBranchData = str(self.BranchList[0])
        CurrBranchData = CurrBranchData.split(" ")
        CurrBranchData = CurrBranchData[1].replace("'","")
        self.Current_BranchName = CurrBranchData.strip()
        #---

        print ("Checking for: {}".format(self.Previous_BranchName))
        if self.Previous_BranchName in str(self.BranchList):
            print ("\tBranch Exists: \"{}\"".format(self.Previous_BranchName))
            self.Previous_BranchStatus = True
        else:
            print ("\tBranch Missing: \"{}\"".format(self.Previous_BranchName))
            self.Previous_BranchStatus = False

    def CheckFileDiff(self,DisplayMSG=False):
        print("\nChecking File(s): {}".format(self.CheckFile))

        SourceBranch = self.Current_BranchName
        TargetBranch = self.Previous_BranchName

        if self.Previous_BranchStatus:
            self.RunParameters = ""
            self.RunParameters = "{} --unified=0".format(self.RunParameters)
            self.RunParameters = "{} --output={}".format(self.RunParameters, self.Checkfile_Report)
            self.RunParameters = "{} --ignore-cr-at-eol".format(self.RunParameters)
            self.RunParameters = "{} --ignore-space-at-eol".format(self.RunParameters)
            self.RunParameters = "{} --ignore-all-space".format(self.RunParameters)
            self.RunParameters = "{} --ignore-blank-lines".format(self.RunParameters)
            self.RunParameters = "{} --function-context".format(self.RunParameters)
            self.RunParameters = "{} --no-prefix".format(self.RunParameters)

            cmd = ("git diff {} {} {} -- {}".format(self.RunParameters, SourceBranch, TargetBranch, self.CheckFile))

            try:
                self.CheckFile_DATA_RAW = self.subprocess.run(cmd, shell=True, capture_output=True)
            except:
                print("Unable to check diff from branches")

            # print(self.CheckFile_DATA_RAW.stdout)
            # print(self.CheckFile_DATA_RAW.stderr)

            print ("\nGenerated feature flag report: {}".format(self.Checkfile_Report))
            print ("----------------------------------------")
            ConfigReport = open(self.Checkfile_Report)
            print(ConfigReport.read())
            print ("----------------------------------------")
        else:
            print ("\t\"{}\" branch is not present in Git".format(TargetBranch))
            print ("\nCurrent Config: {}".format(self.CheckFile))
            print ("----------------------------------------")
            CurrentConfig = open(self.CheckFile)
            print(CurrentConfig.read())
            print ("----------------------------------------")

    def CreateReleaseBranch(self,DisplayMSG=False,ReleaseBranch=""):
        print("Creating Release Branch: {}".format(ReleaseBranch))

        if ReleaseBranch:
            print ("Creating...")
        else:
            print ("Invalid")

class CodeFreeze_FeatureFlags:
    className = "CodeFreeze_FeatureFlags"
    className_string = "Code Freeze - Feature Flags"
    classPrefix = "Feature Flags"

    import csv

    def __init__(self,DisplayMSG=False):
        self.FileName = "FF.csv"
        self.Folder = "featureflags"
        self.Report = "{}.Report.txt".format(self.FileName)

        self.Path = os.path.abspath(os.path.join(RepoRoot, self.Folder))
        self.FullName = os.path.abspath(os.path.join(self.Path, self.FileName))
        self.Validate = os.path.exists(self.FullName)


    def DisplayClassInfo(self,DisplayMSG=False):
        print ("")
        print ("{} (Path): {}".format(self.classPrefix, self.Path))
        print ("{} (File Name): {}".format(self.classPrefix, self.FileName))
        print ("{} (Full Name): {}".format(self.classPrefix, self.FullName))
        print ("{} (Validate): {}".format(self.classPrefix, self.Validate))

# ------
ScriptRoot = os.path.dirname(os.path.realpath('__file__'))
# print ("Script Root: {}".format(ScriptRoot))
# ------

GIT_Info = CodeFreeze_GIT()
# GIT_Info.DisplayClassInfo(DisplayMSG=True)

Release_Info = CodeFreeze_ReleaseInfo()
# Release_Info.DisplayClassInfo(DisplayMSG=True)

Release_PLIST = CodeFreeze_PList()
# Release_PLIST.DisplayClassInfo(DisplayMSG=True)

Release_FF = CodeFreeze_FeatureFlags()
# Release_FF.DisplayClassInfo(DisplayMSG=True)

Release_Info.ReleaseInformationData(CurrentVersion=Release_PLIST.Current_release_version)

MSG_CURRENT = "This branch is currently set for: {}.".format(Release_Info.Current_release_branch)
MSG_NEXT = "The next release is set for: {}.".format(Release_Info.Next_release_branch)
MSG_Proceed = "Would you like to proceed in creating the release and update to the next version? (y/n) "

INPUT_ProceedwithRelease = input("\n{} \n{}  \n{}".format(MSG_CURRENT, MSG_NEXT, MSG_Proceed))

if INPUT_ProceedwithRelease.lower() == "y":
    print ("\n1. Create a separate Git branch to represent current release\n")
    GIT_Info.CreateReleaseBranch(ReleaseBranch=Release_Info.Next_release_branch)

    print ("\n2. Generate a feature flag report\n")
    GIT_Info.Previous_BranchName = Release_Info.Previous_release_branch
    GIT_Info.CheckBranch()

    GIT_Info.CheckFile = Release_FF.FullName
    GIT_Info.Checkfile_Report = Release_FF.Report

    GIT_Info.CheckFileDiff()

    print ("\n3. After performing code freeze, make sure the release file release.plist is updated to reflect the next release name and version in the base branch.\n")
    Release_PLIST.Next_release_name = Release_Info.Next_release_name
    Release_PLIST.Next_release_version = Release_Info.Next_release_version
    Release_PLIST.WriteList()

else:
    print ("\n\t\t\t\tHave a Nice Day!\n")