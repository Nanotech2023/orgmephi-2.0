import { HttpEvent, HttpParams, HttpResponse } from '@angular/common/http'
import {
    RequestGroupAdd,
    RequestLogin,
    RequestPasswordAdmin,
    RequestPasswordSelf,
    RequestRegistration,
    RequestUserGroupsAdd,
    RequestUserGroupsRemove,
    RequestUserRole,
    RequestUserType,
    ResponseGroupAll,
    ResponseInfoCountries,
    ResponseInfoUniversities,
    ResponseUserAdminGroup,
    ResponseUserAll,
    ResponseUserByGroup,
    ResponseUserSelfGroup,
    TypeAuthCredentials,
    TypeCSRFPair,
    TypeGroup,
    TypePersonalInfo,
    TypePreregisterInfo,
    TypeStudentInfo,
    TypeUserInfo
} from '@/auth/api/models'
import { Observable } from 'rxjs'


export interface AuthService
{
    addToHttpParams( httpParams: HttpParams, value: any, key?: string ): HttpParams

    addToHttpParamsRecursive( httpParams: HttpParams, value?: any, key?: string ): HttpParams

    /**
     * Add a group
     * Add a group, only for admins
     * @param requestGroupAdd
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupAddPost( requestGroupAdd: RequestGroupAdd, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeGroup>;

    groupAddPost( requestGroupAdd: RequestGroupAdd, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeGroup>>;

    groupAddPost( requestGroupAdd: RequestGroupAdd, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeGroup>>;

    groupAddPost( requestGroupAdd: RequestGroupAdd, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get all groups
     * Get all group list, only for admins and creators
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupAllGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseGroupAll>;

    groupAllGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseGroupAll>>;

    groupAllGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseGroupAll>>;

    groupAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get any group
     * Get any group, only for admins and creators
     * @param groupId Id of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupGroupIdGet( groupId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeGroup>;

    groupGroupIdGet( groupId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeGroup>>;

    groupGroupIdGet( groupId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeGroup>>;

    groupGroupIdGet( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Delete a group
     * Add a group, only for admins
     * @param groupId ID of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupGroupIdRemovePost( groupId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    groupGroupIdRemovePost( groupId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    groupGroupIdRemovePost( groupId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    groupGroupIdRemovePost( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get known country list
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    infoCountriesGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseInfoCountries>;

    infoCountriesGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseInfoCountries>>;

    infoCountriesGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseInfoCountries>>;

    infoCountriesGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get known university list
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    infoUniversitiesGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseInfoUniversities>;

    infoUniversitiesGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseInfoUniversities>>;

    infoUniversitiesGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseInfoUniversities>>;

    infoUniversitiesGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Authenticate a user
     * @param requestLogin
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    loginPost( requestLogin: RequestLogin, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeCSRFPair>;

    loginPost( requestLogin: RequestLogin, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeCSRFPair>>;

    loginPost( requestLogin: RequestLogin, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeCSRFPair>>;

    loginPost( requestLogin: RequestLogin, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Logout current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    logoutPost( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    logoutPost( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    logoutPost( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    logoutPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * Register an unconfirmed user with a one-time password
     * Register an unconfirmed user with a one-time password, creators and admins only
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    preregisterPost( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypePreregisterInfo>;

    preregisterPost( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypePreregisterInfo>>;

    preregisterPost( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypePreregisterInfo>>;

    preregisterPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Refresh JWT token for current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    refreshPost( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeCSRFPair>;

    refreshPost( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeCSRFPair>>;

    refreshPost( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeCSRFPair>>;

    refreshPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Register an internal user
     * Register an internal user, admin only
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    registerInternalPost( body: TypeAuthCredentials, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeUserInfo>;

    registerInternalPost( body: TypeAuthCredentials, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeUserInfo>>;

    registerInternalPost( body: TypeAuthCredentials, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeUserInfo>>;

    registerInternalPost( body: TypeAuthCredentials, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Register a new user
     * @param requestRegistration
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    registerPost( requestRegistration: RequestRegistration, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeUserInfo>;

    registerPost( requestRegistration: RequestRegistration, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeUserInfo>>;

    registerPost( requestRegistration: RequestRegistration, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeUserInfo>>;

    registerPost( requestRegistration: RequestRegistration, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get common info for all users
     * Get info about all users, only for admins and creators
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userAllGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseUserAll>;

    userAllGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseUserAll>>;

    userAllGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseUserAll>>;

    userAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get common info for different users
     * Get info about any user by their group, only for admins and creators
     * @param groupId ID of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userByGroupGroupIdGet( groupId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseUserByGroup>;

    userByGroupGroupIdGet( groupId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseUserByGroup>>;

    userByGroupGroupIdGet( groupId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseUserByGroup>>;

    userByGroupGroupIdGet( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get common info for current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeUserInfo>;

    userSelfGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeUserInfo>>;

    userSelfGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeUserInfo>>;

    userSelfGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get groups for current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfGroupsGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseUserSelfGroup>;

    userSelfGroupsGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseUserSelfGroup>>;

    userSelfGroupsGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseUserSelfGroup>>;

    userSelfGroupsGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Change password for current user
     * @param requestPasswordSelf
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get personal info for current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfPersonalGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypePersonalInfo>;

    userSelfPersonalGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypePersonalInfo>>;

    userSelfPersonalGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypePersonalInfo>>;

    userSelfPersonalGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get university student info for current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfUniversityGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypePersonalInfo>;

    userSelfUniversityGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypePersonalInfo>>;

    userSelfUniversityGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypePersonalInfo>>;

    userSelfUniversityGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get common info for a different user
     * Get info about any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeUserInfo>;

    userUserIdGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeUserInfo>>;

    userUserIdGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeUserInfo>>;

    userUserIdGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Assign a user to a group
     * Assign a user to a group, only for admins and creators
     * @param userId Id of the user
     * @param requestUserGroupsAdd
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get groups for a different user
     * Get group list for any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdGroupsGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseUserAdminGroup>;

    userUserIdGroupsGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseUserAdminGroup>>;

    userUserIdGroupsGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseUserAdminGroup>>;

    userUserIdGroupsGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Remove a user from a group
     * Remove a user from a group, only for admins and creators
     * @param userId Id of the user
     * @param requestUserGroupsRemove
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Change password for another user
     * Change password for another user, admins only
     * @param userId Id of the user
     * @param requestPasswordAdmin
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get personal info for a different user
     * Get personal info about any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdPersonalGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypePersonalInfo>;

    userUserIdPersonalGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypePersonalInfo>>;

    userUserIdPersonalGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypePersonalInfo>>;

    userUserIdPersonalGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Set personal info for a user
     * Set personal info about any user by its id, only for admins
     * @param userId Id of the user
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Set the role of any user
     * Set the role of another user, only for admins
     * @param userId Id of the user
     * @param requestUserRole
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Set the type of any user
     * Set the type of another user, only for admins
     * @param userId Id of the user
     * @param requestUserType
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get university student info for a different user
     * Get university student info about any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdUniversityGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeStudentInfo>;

    userUserIdUniversityGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeStudentInfo>>;

    userUserIdUniversityGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeStudentInfo>>;

    userUserIdUniversityGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Set university student info for a user
     * Set university student info about any user by its id, only for admins
     * @param userId Id of the user
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>
}