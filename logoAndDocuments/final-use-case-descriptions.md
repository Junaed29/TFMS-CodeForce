# CSCI Use Case Descriptions

**User Authentication & Login (SRS_REQ_100)**

**Actors**: All users (Admin, HOD, PSM, Lecturer, Management)

**Brief Description**

Users securely log into TFMS. TFMS validates credentials and displays role-specific dashboards.

**Characteristics of Activation**

The use case is activated when a user navigates to the TFMS login page and attempts to authenticate.

**Pre-Condition(s)**

1.  TFMS operational.
2.  Valid user account exists.
3.  User account active.

**Description**

**Basic Flow**:

1.  User navigates to login page. (SRS_REQ_101)
2.  TFMS displays login form. (SRS_REQ_102)
3.  User enters credentials. (SRS_REQ_103)
4.  User clicks "Login" button. If not, **[A1: Forgot Password]**. (SRS_REQ_104)
5.  TFMS validates credentials. If invalid, **[E1: Invalid Credentials]**. (SRS_REQ_105)
6.  TFMS checks if account is locked. If locked, **[E2: Account Locked]**. (SRS_REQ_106)
7.  TFMS checks if first login. If yes, **[A2: First-Time Password Change]**. (SRS_REQ_107)
8.  TFMS creates session and logs login. (SRS_REQ_108)
9.  TFMS displays role-appropriate dashboard. (SRS_REQ_109)
10. Use case ends.

**Alternative Flow**

**A1: Forgot Password**

1.  User clicks "Forgot Password". (SRS_REQ_110)
2.  TFMS sends reset link to email. (SRS_REQ_111)
3.  User resets password.
4.  The use case continues.

**A2: First-Time Password Change**

1.  TFMS detects unmodified initial password. (SRS_REQ_112)
2.  TFMS displays password change form. (SRS_REQ_113)
3.  User enters new password **[R1: Password Policy]**. (SRS_REQ_114)
4.  TFMS updates password.
5.  The use case continues.

**Exception Flow**

**E1: Invalid Credentials**

1.  Credentials incorrect. (SRS_REQ_115)
2.  TFMS increments failed attempt counter. (SRS_REQ_116)
3.  After three attempts, account locked **[E2: Account Locked]**. (SRS_REQ_117)
4.  TFMS displays error message "Invalid username or password".
5.  The TFMS logs the failed attempt.
6.  The use case ends.

**E2: Account Locked**

1.  Account locked. (SRS_REQ_118)
2.  TFMS displays lock message "Your account is locked. Contact the TFMS Administrator". (SRS_REQ_119)
3.  Admin intervention required.
4.  The use case ends.

**Post-Condition(s)**

-   User authenticated.
-   Role-appropriate dashboard displayed.
-   Login attempt logged.

**Rule(s) and Constraint(s)**

-   **R1**: Password policy: 8-16 alphanumeric characters.
-   **R2**: Account locks after three failed attempts.
-   **R3**: Dashboard displays based on role.

***

**3.2.12 Configure TFMS Parameters & Master Data Management (SRS_REQ_200)**

**Actor**: System Administrator

**Brief Description**

Admin manages staff records, task forces, System configuration, and user accounts.

**Characteristics of Activation**

The use case is activated when the System Administrator accesses the administration panel to set up or maintain TFMS data.

**Pre-Condition(s)**

1.  Admin logged in.
2.  TFMS operational.

**Description**

**Basic Flow**:

1.  Admin accesses Staff Management. (SRS_REQ_201)
2.  Admin manages staff records (add/edit). (SRS_REQ_202)
3.  TFMS auto-generates Staff IDs **[R5: Automatic Staff ID Generation]**. (SRS_REQ_203)
4.  Admin assigns user roles (Admin, HOD, PSM, Lecturer, Management) **[R1: Role Assignment]**. (SRS_REQ_204)
5.  TFMS creates accounts with temporary passwords. (SRS_REQ_205)
6.  Admin can reset passwords and unlock accounts. (SRS_REQ_206)
7.  Admin can deactivate staff **[A1: Deactivate Staff]**. (SRS_REQ_207)
8.  Admin creates and manages task forces. (SRS_REQ_208)
9.  TFMS auto-generates Task Force IDs **[R6: Automatic Task Force ID Generation]**. (SRS_REQ_209)
10. Admin configures TFMS parameters **[R4: Workload Threshold Constraints]**. (SRS_REQ_210)
11. Admin views audit logs. (SRS_REQ_211)
12. TFMS logs all actions **[R3: Audit Trail Recording]**. (SRS_REQ_212)
13. The use case ends.

**Alternative Flow**:

**A1: Deactivate Staff**

1.  Admin deactivates staff. (SRS_REQ_213)
2.  TFMS blocks all access and new assignments **[R2: Staff Status Management]**.
3.  The use case continues.

**A2: Deactivate Task Force**

1.  Admin deactivates task force. (SRS_REQ_214)
2.  TFMS blocks new assignments.
3.  The use case continues.

**Post-Condition(s)**

-   Staff and task force data managed.
-   TFMS configured.
-   User accounts are created.
-   All Actions logged.

**Rule(s) and Constraint(s)**

-   **R1**: Role-based dashboard.
-   **R2**: Only active staff can access TFMS.
-   **R3**: All admin actions logged.
-   **R4**: Min weightage < Max weightage.
-   **R5**: Auto-generate Staff IDs.
-   **R6**: Auto-generate Task Force IDs.

***

**3.2.13 Use Case Manage Task Force Membership & Workload Distribution (SRS_REQ_300)**

**Actor**: HOD

**Brief Description**

HOD manages task force membership, checks workload, submits for approval.

**Characteristics of Activation**

The use case is activated when a HOD accesses the task force management section to assign or modify memberships.

**Pre-Condition(s)**

1.  HOD logged in.
2.  Task forces exist.
3.  Staff records available.

**Description**

**Basic Flow**:

1.  HOD accesses Task Force Management. (SRS_REQ_301)
2.  TFMS displays department task forces. (SRS_REQ_302)
3.  HOD filters and selects task force. (SRS_REQ_303)
4.  TFMS shows current members. (SRS_REQ_304)
5.  HOD adds/removes members **[R1: Only active staff]**. (SRS_REQ_305)
6.  TFMS calculates workload status. (SRS_REQ_306)
7.  TFMS warns on overload if any member is overloaded **[R2: Workload classified]**. **[A1: Override with Justification]**. (SRS_REQ_307)
8.  HOD submits for approval. (SRS_REQ_308)
9.  TFMS sends to PSM. (SRS_REQ_309)
10. TFMS logs submission. (SRS_REQ_310)
11. The use case ends.

**Alternative Flow**

**A1: Override with Justification**

1.  HOD overrides overload warning. (SRS_REQ_311)
2.  TFMS prompts justification. (SRS_REQ_312)
3.  HOD provides justification.
4.  The use case continues.

**Exception Flow**:

-   No exception flows defined.

**Post-Condition(s)**

1.  Memberships updated.
2.  Workload calculated.
3.  Submission sent to PSM.
4.  All Actions logged.

**Rule(s) and Constraint(s)**

-   **R1**: Only active staff can be assigned.
-   **R2**: Workload classified as Under/Balanced/Over.

***

**3.2.14 Use Case Review & Approve Task Force Assignments (SRS_REQ_400)**

**Actor**: PSM

**Brief Description**

PSM reviews submissions, adjusts assignments, approves or rejects.

**Characteristics of Activation**

The use case is activated when the PSM/HR Officer accesses the approval section after departments have submitted their task force assignments.

**Pre-Condition(s)**

1.  PSM logged in.
2.  Submissions exist.

**Description**

**Basic Flow**:

1.  PSM accesses Approval Panel. (SRS_REQ_401)
2.  TFMS displays submissions. (SRS_REQ_402)
3.  PSM reviews and adjusts assignments. (SRS_REQ_403)
4.  TFMS recalculates workload. (SRS_REQ_404)
5.  PSM approves or rejects. If rejects **[A1: Reject Submission]**. (SRS_REQ_405)
6.  TFMS locks approved assignments **[R2: Approval Lock]**. (SRS_REQ_406)
7.  TFMS logs actions **[R3: Audit Trail]**. (SRS_REQ_407)
8.  The use case ends.

**Alternative Flow**:

**A1: Reject Submission**

1.  PSM rejects submission. (SRS_REQ_408)
2.  PSM enters feedback. (SRS_REQ_409)
3.  TFMS logs rejection.
4.  The use case continues.

**Exception Flow**:

-   No exception flows defined.

**Post-Condition(s)**

1.  Assignments approved or rejected.
2.  Workload finalized.
3.  Actions logged.

**Rule(s) and Constraint(s)**

-   **R1**: Adjustments require justification.
-   **R2**: Approved assignments are locked.
-   **R3**: All actions logged.

***

**3.2.15 Use Case Access Personal Task Force Portfolio (SRS_REQ_500)**

**Actor**: Lecturer

**Brief Description**

Lecturer views assignments, workload status, history, submits remarks.

**Characteristics of Activation**

The use case is activated when a lecturer logs in and accesses their personal dashboard to view task force assignments.

**Pre-Condition(s)**

1.  Lecturer logged in.
2.  Assignments approved.

**Description**

**Basic Flow**:

1.  Lecturer accesses "My Portfolio" section. (SRS_REQ_501)
2.  TFMS displays a dashboard showing all assignments and status **[R1: Personal Data Access]**. (SRS_REQ_502)
3.  Lecturer views history **[R2: Historical Record Retention]**. (SRS_REQ_503)
4.  Lecturer downloads the report **[E1: Download Failure]**. (SRS_REQ_504)
5.  Lecturer submits remarks. (SRS_REQ_505)
6.  TFMS notifies HOD/PSM. (SRS_REQ_506)
7.  The use case ends.

**Alternative Flow**

**A1: No Current Assignments**

1.  The lecturer accesses "My Portfolio" but has no assignments in the current session. (SRS_REQ_507)
2.  The TFMS displays: "You have no task force assignments in the current session." (SRS_REQ_508)
3.  The use case continues.

**Exception Flow**

**E1: Download Failure**

1.  PDF generation fails. (SRS_REQ_509)
2.  TFMS displays error.
3.  The use case ends.

**Post-Condition(s)**

1.  Assignments viewed.
2.  Summary downloaded (optional).
3.  Remarks submitted (optional).

**Rule(s) and Constraint(s)**

-   **R1**: Lecturers access own data only.
-   **R2**: Historical records retained.

***

**3.2.16 Use Case Generate Executive Reports & Analytics (SRS_REQ_600)**

**Actor**: Faculty Management

**Brief Description**

Management views dashboards, analyses data, generates reports.

**Characteristics of Activation**

The use case is activated when Faculty Management accesses the reports and analytics section for planning or strategic reviews.

**Pre-Condition(s)**

1.  Management logged in.
2.  Assignments approved.

**Description**

**Basic Flow**:

1.  Management accesses Executive Reports. (SRS_REQ_601)
2.  TFMS displays dashboard. (SRS_REQ_602)
3.  Management drills down to departments. (SRS_REQ_603)
4.  Management generates report. (SRS_REQ_604)
5.  TFMS exports report. (SRS_REQ_605)
6.  TFMS logs activity. (SRS_REQ_606)
7.  The use case ends.

**Alternative Flow**

-   No alternative flows defined.

**Exception Flow**

-   No exception flows defined.

**Post-Conditions**:

-   Dashboard viewed.
-   Report generated.

**Rules and Constraints**:

-   **R1**: Drill-down to department level.
-   **R2**: Reports exportable in PDF/Excel.