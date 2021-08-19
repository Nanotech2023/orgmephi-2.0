import { HttpEvent, HttpParams, HttpResponse } from '@angular/common/http'
import {
    RequestGroupAdd,
    RequestLogin, RequestPasswordAdmin, RequestPasswordSelf,
    RequestRegistrationSchool,
    RequestRegistrationUniversity, RequestUserGroupsAdd, RequestUserGroupsRemove, RequestUserRole, RequestUserType,
    ResponseGroupAll,
    ResponseInfoCountries,
    ResponseInfoUniversities, ResponseUserAdminGroup,
    ResponseUserAll,
    ResponseUserByGroup,
    ResponseUserSelfGroup,
    TypeAuthCredentials,
    TypeCSRFPair,
    TypeGroup, TypePersonalInfo,
    TypePreregisterInfo, TypeStudentInfo,
    TypeUserInfo
} from '@/auth/api/models'
import { Observable } from 'rxjs'
import { Configuration } from '@/shared/configuration'


export abstract class AuthService
{
    public configuration = new Configuration()

    protected constructor( configuration: Configuration )
    {
        if ( configuration )
        {
            this.configuration = configuration
        }
        this.configuration.withCredentials = true
    }

    abstract addToHttpParams( httpParams: HttpParams, value: any, key?: string ): HttpParams

    abstract addToHttpParamsRecursive( httpParams: HttpParams, value?: any, key?: string ): HttpParams

    /**
     * Add a group
     * Add a group, only for admins
     * @param requestGroupAdd
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract groupAddPost( requestGroupAdd: RequestGroupAdd, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeGroup>;

    abstract groupAddPost( requestGroupAdd: RequestGroupAdd, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeGroup>>;

    abstract groupAddPost( requestGroupAdd: RequestGroupAdd, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeGroup>>;

    abstract groupAddPost( requestGroupAdd: RequestGroupAdd, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get all groups
     * Get all group list, only for admins and creators
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract groupAllGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseGroupAll>;

    abstract groupAllGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseGroupAll>>;

    abstract groupAllGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseGroupAll>>;

    abstract groupAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get any group
     * Get any group, only for admins and creators
     * @param groupId Id of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract groupGroupIdGet( groupId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeGroup>;

    abstract groupGroupIdGet( groupId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeGroup>>;

    abstract groupGroupIdGet( groupId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeGroup>>;

    abstract groupGroupIdGet( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Delete a group
     * Add a group, only for admins
     * @param groupId ID of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract groupGroupIdRemovePost( groupId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract groupGroupIdRemovePost( groupId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract groupGroupIdRemovePost( groupId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract groupGroupIdRemovePost( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get known country list
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract infoCountriesGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseInfoCountries>;

    abstract infoCountriesGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseInfoCountries>>;

    abstract infoCountriesGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseInfoCountries>>;

    abstract infoCountriesGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get known university list
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract infoUniversitiesGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseInfoUniversities>;

    abstract infoUniversitiesGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseInfoUniversities>>;

    abstract infoUniversitiesGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseInfoUniversities>>;

    abstract infoUniversitiesGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Authenticate a user
     * @param requestLogin
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract loginPost( requestLogin: RequestLogin, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeCSRFPair>;

    abstract loginPost( requestLogin: RequestLogin, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeCSRFPair>>;

    abstract loginPost( requestLogin: RequestLogin, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeCSRFPair>>;

    abstract loginPost( requestLogin: RequestLogin, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Logout current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract logoutPost( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract logoutPost( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract logoutPost( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract logoutPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * Register an unconfirmed user with a one-time password
     * Register an unconfirmed user with a one-time password, creators and admins only
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract preregisterPost( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypePreregisterInfo>;

    abstract preregisterPost( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypePreregisterInfo>>;

    abstract preregisterPost( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypePreregisterInfo>>;

    abstract preregisterPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Refresh JWT token for current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract refreshPost( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeCSRFPair>;

    abstract refreshPost( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeCSRFPair>>;

    abstract refreshPost( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeCSRFPair>>;

    abstract refreshPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Register an internal user
     * Register an internal user, admin only
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract registerInternalPost( body: TypeAuthCredentials, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeUserInfo>;

    abstract registerInternalPost( body: TypeAuthCredentials, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeUserInfo>>;

    abstract registerInternalPost( body: TypeAuthCredentials, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeUserInfo>>;

    abstract registerInternalPost( body: TypeAuthCredentials, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Register a new school student
     * @param requestRegistrationSchool
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract registerSchoolPost( requestRegistrationSchool: RequestRegistrationSchool, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeUserInfo>;

    abstract registerSchoolPost( requestRegistrationSchool: RequestRegistrationSchool, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeUserInfo>>;

    abstract registerSchoolPost( requestRegistrationSchool: RequestRegistrationSchool, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeUserInfo>>;

    abstract registerSchoolPost( requestRegistrationSchool: RequestRegistrationSchool, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Register a new university student
     * @param requestRegistrationUniversity
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract registerUniversityPost( requestRegistrationUniversity: RequestRegistrationUniversity, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeUserInfo>;

    abstract registerUniversityPost( requestRegistrationUniversity: RequestRegistrationUniversity, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeUserInfo>>;

    abstract registerUniversityPost( requestRegistrationUniversity: RequestRegistrationUniversity, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeUserInfo>>;

    abstract registerUniversityPost( requestRegistrationUniversity: RequestRegistrationUniversity, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get common info for all users
     * Get info about all users, only for admins and creators
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAllGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseUserAll>;

    abstract userAllGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseUserAll>>;

    abstract userAllGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseUserAll>>;

    abstract userAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get common info for different users
     * Get info about any user by their group, only for admins and creators
     * @param groupId ID of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userByGroupGroupIdGet( groupId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseUserByGroup>;

    abstract userByGroupGroupIdGet( groupId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseUserByGroup>>;

    abstract userByGroupGroupIdGet( groupId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseUserByGroup>>;

    abstract userByGroupGroupIdGet( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get common info for current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userSelfGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeUserInfo>;

    abstract userSelfGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeUserInfo>>;

    abstract userSelfGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeUserInfo>>;

    abstract userSelfGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get groups for current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userSelfGroupsGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseUserSelfGroup>;

    abstract userSelfGroupsGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseUserSelfGroup>>;

    abstract userSelfGroupsGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseUserSelfGroup>>;

    abstract userSelfGroupsGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Change password for current user
     * @param requestPasswordSelf
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get personal info for current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userSelfPersonalGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypePersonalInfo>;

    abstract userSelfPersonalGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypePersonalInfo>>;

    abstract userSelfPersonalGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypePersonalInfo>>;

    abstract userSelfPersonalGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get university student info for current user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userSelfUniversityGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypePersonalInfo>;

    abstract userSelfUniversityGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypePersonalInfo>>;

    abstract userSelfUniversityGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypePersonalInfo>>;

    abstract userSelfUniversityGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get common info for a different user
     * Get info about any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeUserInfo>;

    abstract userUserIdGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeUserInfo>>;

    abstract userUserIdGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeUserInfo>>;

    abstract userUserIdGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Assign a user to a group
     * Assign a user to a group, only for admins and creators
     * @param userId Id of the user
     * @param requestUserGroupsAdd
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get groups for a different user
     * Get group list for any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdGroupsGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ResponseUserAdminGroup>;

    abstract userUserIdGroupsGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ResponseUserAdminGroup>>;

    abstract userUserIdGroupsGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ResponseUserAdminGroup>>;

    abstract userUserIdGroupsGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Remove a user from a group
     * Remove a user from a group, only for admins and creators
     * @param userId Id of the user
     * @param requestUserGroupsRemove
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Change password for another user
     * Change password for another user, admins only
     * @param userId Id of the user
     * @param requestPasswordAdmin
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get personal info for a different user
     * Get personal info about any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdPersonalGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypePersonalInfo>;

    abstract userUserIdPersonalGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypePersonalInfo>>;

    abstract userUserIdPersonalGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypePersonalInfo>>;

    abstract userUserIdPersonalGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Set personal info for a user
     * Set personal info about any user by its id, only for admins
     * @param userId Id of the user
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Set the role of any user
     * Set the role of another user, only for admins
     * @param userId Id of the user
     * @param requestUserRole
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Set the type of any user
     * Set the type of another user, only for admins
     * @param userId Id of the user
     * @param requestUserType
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get university student info for a different user
     * Get university student info about any user by its id, only for admins and creators
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdUniversityGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TypeStudentInfo>;

    abstract userUserIdUniversityGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TypeStudentInfo>>;

    abstract userUserIdUniversityGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TypeStudentInfo>>;

    abstract userUserIdUniversityGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Set university student info for a user
     * Set university student info about any user by its id, only for admins
     * @param userId Id of the user
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>
}