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
    ResponseGroup,
    ResponseGroupAdd,
    ResponseGroupAll,
    ResponseInfoCountries,
    ResponseInfoUniversities,
    ResponseLogin,
    ResponsePersonalAdminGet,
    ResponsePersonalSelf,
    ResponsePreregister,
    ResponseRefresh,
    ResponseRegistration,
    ResponseRegistrationInternal,
    ResponseUniversityAdminGet,
    ResponseUniversitySelf,
    ResponseUserAdmin,
    ResponseUserAdminGroup,
    ResponseUserAll,
    ResponseUserByGroup,
    ResponseUserSelf,
    ResponseUserSelfGroup,
    TypeAuthCredentials,
    TypePersonalInfo,
    TypeStudentInfo
} from '@/auth/models'
import { Observable } from 'rxjs'
import { HttpEvent, HttpResponse } from '@angular/common/http'


export interface AuthService
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
    groupAddPost( body: RequestGroupAdd, observe?: 'body', reportProgress?: boolean ): Observable<ResponseGroupAdd>;

    groupAddPost( body: RequestGroupAdd, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseGroupAdd>>;

    groupAddPost( body: RequestGroupAdd, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseGroupAdd>>;

    groupAddPost( body: RequestGroupAdd, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get all groups
     * Get all group list, only for admins and creators
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupAllGet( observe?: 'body', reportProgress?: boolean ): Observable<ResponseGroupAll>;

    groupAllGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseGroupAll>>;

    groupAllGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseGroupAll>>;

    groupAllGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get any group
     * Get any group, only for admins and creators
     * @param groupId Id of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupGroupIdGet( groupId: number, observe?: 'body', reportProgress?: boolean ): Observable<ResponseGroup>;

    groupGroupIdGet( groupId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseGroup>>;

    groupGroupIdGet( groupId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseGroup>>;

    groupGroupIdGet( groupId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Delete a group
     * Add a group, only for admins
     * @param groupId ID of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    groupGroupIdRemovePost( groupId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    groupGroupIdRemovePost( groupId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    groupGroupIdRemovePost( groupId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    groupGroupIdRemovePost( groupId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get known country list
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    infoCountriesGet( observe?: 'body', reportProgress?: boolean ): Observable<ResponseInfoCountries>;

    infoCountriesGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseInfoCountries>>;

    infoCountriesGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseInfoCountries>>;

    infoCountriesGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get known university list
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    infoUniversitiesGet( observe?: 'body', reportProgress?: boolean ): Observable<ResponseInfoUniversities>;

    infoUniversitiesGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseInfoUniversities>>;

    infoUniversitiesGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseInfoUniversities>>;

    infoUniversitiesGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Authenticate a user
     *
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    loginPost( body: RequestLogin, observe?: 'body', reportProgress?: boolean ): Observable<ResponseLogin>;

    loginPost( body: RequestLogin, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseLogin>>;

    loginPost( body: RequestLogin, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseLogin>>;

    loginPost( body: RequestLogin, observe: any, reportProgress: boolean ): Observable<any>

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
    preregisterPost( observe?: 'body', reportProgress?: boolean ): Observable<ResponsePreregister>;

    preregisterPost( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponsePreregister>>;

    preregisterPost( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponsePreregister>>;

    preregisterPost( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Refresh JWT token for current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    refreshPost( observe?: 'body', reportProgress?: boolean ): Observable<ResponseRefresh>;

    refreshPost( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseRefresh>>;

    refreshPost( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseRefresh>>;

    refreshPost( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Register an internal user
     * Register an internal user, admin only
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    registerInternalPost( body: TypeAuthCredentials, observe?: 'body', reportProgress?: boolean ): Observable<ResponseRegistrationInternal>;

    registerInternalPost( body: TypeAuthCredentials, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseRegistrationInternal>>;

    registerInternalPost( body: TypeAuthCredentials, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseRegistrationInternal>>;

    registerInternalPost( body: TypeAuthCredentials, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Register a new user
     *
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    registerPost( body: RequestRegistration, observe?: 'body', reportProgress?: boolean ): Observable<ResponseRegistration>;

    registerPost( body: RequestRegistration, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseRegistration>>;

    registerPost( body: RequestRegistration, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseRegistration>>;

    registerPost( body: RequestRegistration, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get common info for all users
     * Get info about all users, only for admins and creators
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userAllGet( observe?: 'body', reportProgress?: boolean ): Observable<ResponseUserAll>;

    userAllGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseUserAll>>;

    userAllGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseUserAll>>;

    userAllGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get common info for different users
     * Get info about any user by their group, only for admins and creators
     * @param groupId ID of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userByGroupGroupIdGet( groupId: number, observe?: 'body', reportProgress?: boolean ): Observable<ResponseUserByGroup>;

    userByGroupGroupIdGet( groupId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseUserByGroup>>;

    userByGroupGroupIdGet( groupId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseUserByGroup>>;

    userByGroupGroupIdGet( groupId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get common info for current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfGet( observe?: 'body', reportProgress?: boolean ): Observable<ResponseUserSelf>;

    userSelfGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseUserSelf>>;

    userSelfGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseUserSelf>>;

    userSelfGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get groups for current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfGroupsGet( observe?: 'body', reportProgress?: boolean ): Observable<ResponseUserSelfGroup>;

    userSelfGroupsGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseUserSelfGroup>>;

    userSelfGroupsGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseUserSelfGroup>>;

    userSelfGroupsGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Change password for current user
     *
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfPasswordPost( body: RequestPasswordSelf, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userSelfPasswordPost( body: RequestPasswordSelf, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userSelfPasswordPost( body: RequestPasswordSelf, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userSelfPasswordPost( body: RequestPasswordSelf, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get personal info for current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfPersonalGet( observe?: 'body', reportProgress?: boolean ): Observable<ResponsePersonalSelf>;

    userSelfPersonalGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponsePersonalSelf>>;

    userSelfPersonalGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponsePersonalSelf>>;

    userSelfPersonalGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get university student info for current user
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userSelfUniversityGet( observe?: 'body', reportProgress?: boolean ): Observable<ResponseUniversitySelf>;

    userSelfUniversityGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseUniversitySelf>>;

    userSelfUniversityGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseUniversitySelf>>;

    userSelfUniversityGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get common info for a different user
     * Get info about any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdGet( userId: number, observe?: 'body', reportProgress?: boolean ): Observable<ResponseUserAdmin>;

    userUserIdGet( userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseUserAdmin>>;

    userUserIdGet( userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseUserAdmin>>;

    userUserIdGet( userId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Assign a user to a group
     * Assign a user to a group, only for admins and creators
     * @param body
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdGroupsAddPost( body: RequestUserGroupsAdd, userId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userUserIdGroupsAddPost( body: RequestUserGroupsAdd, userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userUserIdGroupsAddPost( body: RequestUserGroupsAdd, userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userUserIdGroupsAddPost( body: RequestUserGroupsAdd, userId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get groups for a different user
     * Get group list for any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdGroupsGet( userId: number, observe?: 'body', reportProgress?: boolean ): Observable<ResponseUserAdminGroup>;

    userUserIdGroupsGet( userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseUserAdminGroup>>;

    userUserIdGroupsGet( userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseUserAdminGroup>>;

    userUserIdGroupsGet( userId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Remove a user from a group
     * Remove a user from a group, only for admins and creators
     * @param body
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdGroupsRemovePost( body: RequestUserGroupsRemove, userId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userUserIdGroupsRemovePost( body: RequestUserGroupsRemove, userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userUserIdGroupsRemovePost( body: RequestUserGroupsRemove, userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userUserIdGroupsRemovePost( body: RequestUserGroupsRemove, userId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Change password for another user
     * Change password for another user, admins only
     * @param body
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdPasswordPost( body: RequestPasswordAdmin, userId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userUserIdPasswordPost( body: RequestPasswordAdmin, userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userUserIdPasswordPost( body: RequestPasswordAdmin, userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userUserIdPasswordPost( body: RequestPasswordAdmin, userId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get personal info for a different user
     * Get personal info about any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdPersonalGet( userId: number, observe?: 'body', reportProgress?: boolean ): Observable<ResponsePersonalAdminGet>;

    userUserIdPersonalGet( userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponsePersonalAdminGet>>;

    userUserIdPersonalGet( userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponsePersonalAdminGet>>;

    userUserIdPersonalGet( userId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set personal info for a user
     * Set personal info about any user by its id, only for admins
     * @param body
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdPersonalPatch( body: TypePersonalInfo, userId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userUserIdPersonalPatch( body: TypePersonalInfo, userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userUserIdPersonalPatch( body: TypePersonalInfo, userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userUserIdPersonalPatch( body: TypePersonalInfo, userId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set the role of any user
     * Set the role of another user, only for admins
     * @param body
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdRolePut( body: RequestUserRole, userId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userUserIdRolePut( body: RequestUserRole, userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userUserIdRolePut( body: RequestUserRole, userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userUserIdRolePut( body: RequestUserRole, userId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set the type of any user
     * Set the type of another user, only for admins
     * @param body
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdTypePut( body: RequestUserType, userId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userUserIdTypePut( body: RequestUserType, userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userUserIdTypePut( body: RequestUserType, userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userUserIdTypePut( body: RequestUserType, userId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get university student info for a different user
     * Get university student info about any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdUniversityGet( userId: number, observe?: 'body', reportProgress?: boolean ): Observable<ResponseUniversityAdminGet>;

    userUserIdUniversityGet( userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseUniversityAdminGet>>;

    userUserIdUniversityGet( userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseUniversityAdminGet>>;

    userUserIdUniversityGet( userId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set university student info for a user
     * Set university student info about any user by its id, only for admins
     * @param body
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userUserIdUniversityPatch( body: TypeStudentInfo, userId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userUserIdUniversityPatch( body: TypeStudentInfo, userId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userUserIdUniversityPatch( body: TypeStudentInfo, userId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userUserIdUniversityPatch( body: TypeStudentInfo, userId: number, observe: any, reportProgress: boolean ): Observable<any>
}