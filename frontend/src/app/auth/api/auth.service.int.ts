import { HttpEvent, HttpResponse } from '@angular/common/http'
import {
    AccountType,
    AddGroup,
    Authentication,
    AuthResponse,
    ChangePassword,
    ChangePasswordAdmin,
    CommonUserInfo,
    GetCountriesResponse,
    GetUniversitiesResponse,
    GroupList,
    GroupType,
    PersonalInfo,
    PersonalInfoUpdate,
    RegisterAuthInfo,
    RegisterConfirm,
    Registration,
    StudentInfo,
    StudentInfoUpdate,
    UpdateGroups,
    UserList,
    UserRole
} from '@/auth/models'
import { Observable } from 'rxjs'


export interface IAuthService
{
    /**
     * @param consumes string[] mime-types
     * @return true: consumes contains 'multipart/form-data', false: otherwise
     */
    canConsumeForm( consumes: string[] ): boolean

    /**
     * Add a group
     * Add a group, only for admins
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupAddPost( body: AddGroup, observe?: 'body', reportProgress?: boolean ): Observable<GroupType>;

    groupAddPost( body: AddGroup, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<GroupType>>;

    groupAddPost( body: AddGroup, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<GroupType>>;

    groupAddPost( body: AddGroup, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get all groups
     * Get all group list, only for admins and creators
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupAllGet( observe?: 'body', reportProgress?: boolean ): Observable<GroupList>;

    groupAllGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<GroupList>>;

    groupAllGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<GroupList>>;

    groupAllGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Delete a group
     * Add a group, only for admins
     * @param body
     * @param id ID of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupIdDeletePost( body: AddGroup, id: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    groupIdDeletePost( body: AddGroup, id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    groupIdDeletePost( body: AddGroup, id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    groupIdDeletePost( body: AddGroup, id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get any group
     * Get any group, only for admins and creators
     * @param id Id of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupIdGet( id: number, observe?: 'body', reportProgress?: boolean ): Observable<GroupType>;

    groupIdGet( id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<GroupType>>;

    groupIdGet( id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<GroupType>>;

    groupIdGet( id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get known country list
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    infoCountriesGet( observe?: 'body', reportProgress?: boolean ): Observable<GetCountriesResponse>;

    infoCountriesGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<GetCountriesResponse>>;

    infoCountriesGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<GetCountriesResponse>>;

    infoCountriesGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get known university list
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    infoUniversitiesGet( observe?: 'body', reportProgress?: boolean ): Observable<GetUniversitiesResponse>;

    infoUniversitiesGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<GetUniversitiesResponse>>;

    infoUniversitiesGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<GetUniversitiesResponse>>;

    infoUniversitiesGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Authenticate a user
     *
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    loginPost( body: Authentication, observe?: 'body', reportProgress?: boolean ): Observable<AuthResponse>;

    loginPost( body: Authentication, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<AuthResponse>>;

    loginPost( body: Authentication, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<AuthResponse>>;

    loginPost( body: Authentication, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Logout current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    logoutPost( observe?: 'body', reportProgress?: boolean ): Observable<any>;

    logoutPost( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    logoutPost( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    logoutPost( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Register an unconfirmed user with a one-time password
     * Register an unconfirmed user with a one-time password, creators and admins only
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    preregisterPost( observe?: 'body', reportProgress?: boolean ): Observable<RegisterConfirm>;

    preregisterPost( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<RegisterConfirm>>;

    preregisterPost( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<RegisterConfirm>>;

    preregisterPost( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Refresh JWT token for current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    refreshPost( observe?: 'body', reportProgress?: boolean ): Observable<AuthResponse>;

    refreshPost( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<AuthResponse>>;

    refreshPost( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<AuthResponse>>;

    refreshPost( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Register an internal user
     * Register an internal user, admin only
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    registerInternalPost( body: RegisterAuthInfo, observe?: 'body', reportProgress?: boolean ): Observable<CommonUserInfo>;

    registerInternalPost( body: RegisterAuthInfo, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonUserInfo>>;

    registerInternalPost( body: RegisterAuthInfo, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonUserInfo>>;

    registerInternalPost( body: RegisterAuthInfo, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Register a new user
     *
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    registerPost( body: Registration, observe?: 'body', reportProgress?: boolean ): Observable<CommonUserInfo>;

    registerPost( body: Registration, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonUserInfo>>;

    registerPost( body: Registration, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonUserInfo>>;

    registerPost( body: Registration, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get common info for all users
     * Get info about all users, only for admins and creators
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userAllGet( observe?: 'body', reportProgress?: boolean ): Observable<UserList>;

    userAllGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UserList>>;

    userAllGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UserList>>;

    userAllGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get common info for different users
     * Get info about any user by their group, only for admins and creators
     * @param id ID of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userByGroupIdGet( id: number, observe?: 'body', reportProgress?: boolean ): Observable<UserList>;

    userByGroupIdGet( id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UserList>>;

    userByGroupIdGet( id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UserList>>;

    userByGroupIdGet( id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get common info for a different user
     * Get info about any user by its id, only for admins and creators
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdGet( id: number, observe?: 'body', reportProgress?: boolean ): Observable<CommonUserInfo>;

    userIdGet( id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonUserInfo>>;

    userIdGet( id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonUserInfo>>;

    userIdGet( id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Assign a user to a group
     * Assign a user to a group, only for admins and creators
     * @param body
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdGroupsAddPost( body: UpdateGroups, id: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userIdGroupsAddPost( body: UpdateGroups, id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userIdGroupsAddPost( body: UpdateGroups, id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userIdGroupsAddPost( body: UpdateGroups, id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get groups for a different user
     * Get group list for any user by its id, only for admins and creators
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdGroupsGet( id: number, observe?: 'body', reportProgress?: boolean ): Observable<GroupList>;

    userIdGroupsGet( id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<GroupList>>;

    userIdGroupsGet( id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<GroupList>>;

    userIdGroupsGet( id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Remove a user from a group
     * Remove a user from a group, only for admins and creators
     * @param body
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdGroupsRemovePost( body: UpdateGroups, id: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userIdGroupsRemovePost( body: UpdateGroups, id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userIdGroupsRemovePost( body: UpdateGroups, id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userIdGroupsRemovePost( body: UpdateGroups, id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Change password for another user
     * Change password for another user, admins only
     * @param body
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdPasswordPost( body: ChangePasswordAdmin, id: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userIdPasswordPost( body: ChangePasswordAdmin, id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userIdPasswordPost( body: ChangePasswordAdmin, id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userIdPasswordPost( body: ChangePasswordAdmin, id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get personal info for a different user
     * Get personal info about any user by its id, only for admins and creators
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdPersonalGet( id: number, observe?: 'body', reportProgress?: boolean ): Observable<PersonalInfo>;

    userIdPersonalGet( id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<PersonalInfo>>;

    userIdPersonalGet( id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<PersonalInfo>>;

    userIdPersonalGet( id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set personal info for a user
     * Set personal info about any user by its id, only for admins
     * @param body
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdPersonalPatch( body: PersonalInfoUpdate, id: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userIdPersonalPatch( body: PersonalInfoUpdate, id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userIdPersonalPatch( body: PersonalInfoUpdate, id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userIdPersonalPatch( body: PersonalInfoUpdate, id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set the role of any user
     * Set the role of another user, only for admins
     * @param body
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdRolePut( body: UserRole, id: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userIdRolePut( body: UserRole, id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userIdRolePut( body: UserRole, id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userIdRolePut( body: UserRole, id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set the type of any user
     * Set the type of another user, only for admins
     * @param body
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdTypePut( body: AccountType, id: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userIdTypePut( body: AccountType, id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userIdTypePut( body: AccountType, id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userIdTypePut( body: AccountType, id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get university student info for a different user
     * Get university student info about any user by its id, only for admins and creators
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdUniversityGet( id: number, observe?: 'body', reportProgress?: boolean ): Observable<StudentInfo>;

    userIdUniversityGet( id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<StudentInfo>>;

    userIdUniversityGet( id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<StudentInfo>>;

    userIdUniversityGet( id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set university student info for a user
     * Set university student info about any user by its id, only for admins
     * @param body
     * @param id Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userIdUniversityPatch( body: StudentInfoUpdate, id: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userIdUniversityPatch( body: StudentInfoUpdate, id: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userIdUniversityPatch( body: StudentInfoUpdate, id: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userIdUniversityPatch( body: StudentInfoUpdate, id: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get common info for current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfGet( observe?: 'body', reportProgress?: boolean ): Observable<CommonUserInfo>;

    userSelfGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonUserInfo>>;

    userSelfGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonUserInfo>>;

    userSelfGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get groups for current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfGroupsGet( observe?: 'body', reportProgress?: boolean ): Observable<GroupList>;

    userSelfGroupsGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<GroupList>>;

    userSelfGroupsGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<GroupList>>;

    userSelfGroupsGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Change password for current user
     *
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfPasswordPost( body: ChangePassword, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userSelfPasswordPost( body: ChangePassword, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userSelfPasswordPost( body: ChangePassword, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userSelfPasswordPost( body: ChangePassword, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get personal info for current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfPersonalGet( observe?: 'body', reportProgress?: boolean ): Observable<PersonalInfo>;

    userSelfPersonalGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<PersonalInfo>>;

    userSelfPersonalGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<PersonalInfo>>;

    userSelfPersonalGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get university student info for current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfUniversityGet( observe?: 'body', reportProgress?: boolean ): Observable<StudentInfo>;

    userSelfUniversityGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<StudentInfo>>;

    userSelfUniversityGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<StudentInfo>>;

    userSelfUniversityGet( observe: any, reportProgress: boolean ): Observable<any>
}