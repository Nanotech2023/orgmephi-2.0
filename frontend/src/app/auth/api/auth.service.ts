import {
    CSRFPairUser,
    Group,
    GroupAddRequestUser,
    GroupListResponseUser,
    InfoCitiesResponseUser,
    InfoCountriesResponseUser,
    InfoRegionsResponseUser,
    InfoUniversitiesResponseUser,
    LoginRequestUser,
    MembershipRequestUser,
    PasswordRequestUser,
    PreregisterResponseUser,
    RegisterInternalRequestUser,
    RoleRequestUser,
    SchoolInfo,
    SchoolInfoInput,
    SchoolRegistrationRequestUser,
    SelfGroupsResponseUser,
    SelfPasswordRequestUser,
    StudentInfo,
    StudentInfoInput,
    TypeRequestUser,
    UniversityRegistrationRequestUser,
    UserFullListResponseUser,
    User,
    UserInfoInput,
    UserInfoRestrictedInput,
    UserListResponseUser
} from '@/auth/api/models'
import { Observable } from 'rxjs'
import { HttpEvent, HttpParams, HttpResponse } from '@angular/common/http'
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

    /**
     * @param groupAddRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminAddGroupPost( groupAddRequestUser: GroupAddRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<Group>;

    abstract userAdminAddGroupPost( groupAddRequestUser: GroupAddRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<Group>>;

    abstract userAdminAddGroupPost( groupAddRequestUser: GroupAddRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<Group>>;

    abstract userAdminAddGroupPost( groupAddRequestUser: GroupAddRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param membershipRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminAddMemberUserIdPost( userId: number, membershipRequestUser: MembershipRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userAdminAddMemberUserIdPost( userId: number, membershipRequestUser: MembershipRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userAdminAddMemberUserIdPost( userId: number, membershipRequestUser: MembershipRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userAdminAddMemberUserIdPost( userId: number, membershipRequestUser: MembershipRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param registerInternalRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminInternalRegisterPost( registerInternalRequestUser: RegisterInternalRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<User>;

    abstract userAdminInternalRegisterPost( registerInternalRequestUser: RegisterInternalRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<User>>;

    abstract userAdminInternalRegisterPost( registerInternalRequestUser: RegisterInternalRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<User>>;

    abstract userAdminInternalRegisterPost( registerInternalRequestUser: RegisterInternalRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param passwordRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminPasswordUserIdPost( userId: number, passwordRequestUser: PasswordRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userAdminPasswordUserIdPost( userId: number, passwordRequestUser: PasswordRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userAdminPasswordUserIdPost( userId: number, passwordRequestUser: PasswordRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userAdminPasswordUserIdPost( userId: number, passwordRequestUser: PasswordRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param userInfoInput
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminPersonalUserIdPatch( userId: number, userInfoInput: UserInfoInput, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userAdminPersonalUserIdPatch( userId: number, userInfoInput: UserInfoInput, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userAdminPersonalUserIdPatch( userId: number, userInfoInput: UserInfoInput, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userAdminPersonalUserIdPatch( userId: number, userInfoInput: UserInfoInput, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminPreregisterPost( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<PreregisterResponseUser>;

    abstract userAdminPreregisterPost( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<PreregisterResponseUser>>;

    abstract userAdminPreregisterPost( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<PreregisterResponseUser>>;

    abstract userAdminPreregisterPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param groupId ID of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminRemoveGroupGroupIdPost( groupId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userAdminRemoveGroupGroupIdPost( groupId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userAdminRemoveGroupGroupIdPost( groupId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userAdminRemoveGroupGroupIdPost( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param membershipRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminRemoveMemberUserIdPost( userId: number, membershipRequestUser: MembershipRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userAdminRemoveMemberUserIdPost( userId: number, membershipRequestUser: MembershipRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userAdminRemoveMemberUserIdPost( userId: number, membershipRequestUser: MembershipRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userAdminRemoveMemberUserIdPost( userId: number, membershipRequestUser: MembershipRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param roleRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminRoleUserIdPut( userId: number, roleRequestUser: RoleRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userAdminRoleUserIdPut( userId: number, roleRequestUser: RoleRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userAdminRoleUserIdPut( userId: number, roleRequestUser: RoleRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userAdminRoleUserIdPut( userId: number, roleRequestUser: RoleRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param schoolInfoInput
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminSchoolUserIdPatch( userId: number, schoolInfoInput: SchoolInfoInput, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userAdminSchoolUserIdPatch( userId: number, schoolInfoInput: SchoolInfoInput, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userAdminSchoolUserIdPatch( userId: number, schoolInfoInput: SchoolInfoInput, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userAdminSchoolUserIdPatch( userId: number, schoolInfoInput: SchoolInfoInput, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param typeRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminTypeUserIdPut( userId: number, typeRequestUser: TypeRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userAdminTypeUserIdPut( userId: number, typeRequestUser: TypeRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userAdminTypeUserIdPut( userId: number, typeRequestUser: TypeRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userAdminTypeUserIdPut( userId: number, typeRequestUser: TypeRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param studentInfoInput
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAdminUniversityUserIdPatch( userId: number, studentInfoInput: StudentInfoInput, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userAdminUniversityUserIdPatch( userId: number, studentInfoInput: StudentInfoInput, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userAdminUniversityUserIdPatch( userId: number, studentInfoInput: StudentInfoInput, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userAdminUniversityUserIdPatch( userId: number, studentInfoInput: StudentInfoInput, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param loginRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAuthLoginPost( loginRequestUser: LoginRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<CSRFPairUser>;

    abstract userAuthLoginPost( loginRequestUser: LoginRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<CSRFPairUser>>;

    abstract userAuthLoginPost( loginRequestUser: LoginRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<CSRFPairUser>>;

    abstract userAuthLoginPost( loginRequestUser: LoginRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAuthLogoutPost( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userAuthLogoutPost( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userAuthLogoutPost( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userAuthLogoutPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userAuthRefreshPost( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<CSRFPairUser>;

    abstract userAuthRefreshPost( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<CSRFPairUser>>;

    abstract userAuthRefreshPost( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<CSRFPairUser>>;

    abstract userAuthRefreshPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userCreatorGroupAllGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<GroupListResponseUser>;

    abstract userCreatorGroupAllGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<GroupListResponseUser>>;

    abstract userCreatorGroupAllGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<GroupListResponseUser>>;

    abstract userCreatorGroupAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param groupId Id of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userCreatorGroupGroupIdGet( groupId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<Group>;

    abstract userCreatorGroupGroupIdGet( groupId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<Group>>;

    abstract userCreatorGroupGroupIdGet( groupId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<Group>>;

    abstract userCreatorGroupGroupIdGet( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userCreatorMembershipUserIdGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<GroupListResponseUser>;

    abstract userCreatorMembershipUserIdGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<GroupListResponseUser>>;

    abstract userCreatorMembershipUserIdGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<GroupListResponseUser>>;

    abstract userCreatorMembershipUserIdGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userCreatorPersonalUserIdGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<User>;

    abstract userCreatorPersonalUserIdGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<User>>;

    abstract userCreatorPersonalUserIdGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<User>>;

    abstract userCreatorPersonalUserIdGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userCreatorSchoolUserIdGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<SchoolInfo>;

    abstract userCreatorSchoolUserIdGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<SchoolInfo>>;

    abstract userCreatorSchoolUserIdGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<SchoolInfo>>;

    abstract userCreatorSchoolUserIdGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userCreatorUniversityUserIdGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<StudentInfo>;

    abstract userCreatorUniversityUserIdGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<StudentInfo>>;

    abstract userCreatorUniversityUserIdGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<StudentInfo>>;

    abstract userCreatorUniversityUserIdGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userCreatorUserAllGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<UserListResponseUser>;

    abstract userCreatorUserAllGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<UserListResponseUser>>;

    abstract userCreatorUserAllGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<UserListResponseUser>>;

    abstract userCreatorUserAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param groupId ID of the group
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userCreatorUserByGroupGroupIdGet( groupId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<UserListResponseUser>;

    abstract userCreatorUserByGroupGroupIdGet( groupId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<UserListResponseUser>>;

    abstract userCreatorUserByGroupGroupIdGet( groupId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<UserListResponseUser>>;

    abstract userCreatorUserByGroupGroupIdGet( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userCreatorUserFullAllGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<UserFullListResponseUser>;

    abstract userCreatorUserFullAllGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<UserFullListResponseUser>>;

    abstract userCreatorUserFullAllGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<UserFullListResponseUser>>;

    abstract userCreatorUserFullAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param userId Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userCreatorUserUserIdGet( userId: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<User>;

    abstract userCreatorUserUserIdGet( userId: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<User>>;

    abstract userCreatorUserUserIdGet( userId: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<User>>;

    abstract userCreatorUserUserIdGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userProfileGroupsGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<SelfGroupsResponseUser>;

    abstract userProfileGroupsGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<SelfGroupsResponseUser>>;

    abstract userProfileGroupsGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<SelfGroupsResponseUser>>;

    abstract userProfileGroupsGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param selfPasswordRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userProfilePasswordPost( selfPasswordRequestUser: SelfPasswordRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userProfilePasswordPost( selfPasswordRequestUser: SelfPasswordRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userProfilePasswordPost( selfPasswordRequestUser: SelfPasswordRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userProfilePasswordPost( selfPasswordRequestUser: SelfPasswordRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userProfilePersonalGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<User>;

    abstract userProfilePersonalGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<User>>;

    abstract userProfilePersonalGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<User>>;

    abstract userProfilePersonalGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param userInfoRestrictedInput
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userProfilePersonalPatch( userInfoRestrictedInput: UserInfoRestrictedInput, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userProfilePersonalPatch( userInfoRestrictedInput: UserInfoRestrictedInput, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userProfilePersonalPatch( userInfoRestrictedInput: UserInfoRestrictedInput, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userProfilePersonalPatch( userInfoRestrictedInput: UserInfoRestrictedInput, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userProfileSchoolGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<SchoolInfo>;

    abstract userProfileSchoolGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<SchoolInfo>>;

    abstract userProfileSchoolGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<SchoolInfo>>;

    abstract userProfileSchoolGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param schoolInfoInput
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userProfileSchoolPatch( schoolInfoInput: SchoolInfoInput, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userProfileSchoolPatch( schoolInfoInput: SchoolInfoInput, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userProfileSchoolPatch( schoolInfoInput: SchoolInfoInput, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userProfileSchoolPatch( schoolInfoInput: SchoolInfoInput, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userProfileUniversityGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<StudentInfo>;

    abstract userProfileUniversityGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<StudentInfo>>;

    abstract userProfileUniversityGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<StudentInfo>>;

    abstract userProfileUniversityGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param studentInfoInput
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userProfileUniversityPatch( studentInfoInput: StudentInfoInput, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>;

    abstract userProfileUniversityPatch( studentInfoInput: StudentInfoInput, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>;

    abstract userProfileUniversityPatch( studentInfoInput: StudentInfoInput, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>;

    abstract userProfileUniversityPatch( studentInfoInput: StudentInfoInput, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userProfileUserGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<User>;

    abstract userProfileUserGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<User>>;

    abstract userProfileUserGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<User>>;

    abstract userProfileUserGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param region Region name
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userRegistrationInfoCitiesRegionGet( region: string, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<InfoCitiesResponseUser>;

    abstract userRegistrationInfoCitiesRegionGet( region: string, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<InfoCitiesResponseUser>>;

    abstract userRegistrationInfoCitiesRegionGet( region: string, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<InfoCitiesResponseUser>>;

    abstract userRegistrationInfoCitiesRegionGet( region: string, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userRegistrationInfoCountriesGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<InfoCountriesResponseUser>;

    abstract userRegistrationInfoCountriesGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<InfoCountriesResponseUser>>;

    abstract userRegistrationInfoCountriesGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<InfoCountriesResponseUser>>;

    abstract userRegistrationInfoCountriesGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userRegistrationInfoRegionsGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<InfoRegionsResponseUser>;

    abstract userRegistrationInfoRegionsGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<InfoRegionsResponseUser>>;

    abstract userRegistrationInfoRegionsGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<InfoRegionsResponseUser>>;

    abstract userRegistrationInfoRegionsGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userRegistrationInfoUniversitiesGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<InfoUniversitiesResponseUser>;

    abstract userRegistrationInfoUniversitiesGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<InfoUniversitiesResponseUser>>;

    abstract userRegistrationInfoUniversitiesGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<InfoUniversitiesResponseUser>>;

    abstract userRegistrationInfoUniversitiesGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Register a new school student
     * @param schoolRegistrationRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userRegistrationSchoolPost( schoolRegistrationRequestUser: SchoolRegistrationRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<User>;

    abstract userRegistrationSchoolPost( schoolRegistrationRequestUser: SchoolRegistrationRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<User>>;

    abstract userRegistrationSchoolPost( schoolRegistrationRequestUser: SchoolRegistrationRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<User>>;

    abstract userRegistrationSchoolPost( schoolRegistrationRequestUser: SchoolRegistrationRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * @param universityRegistrationRequestUser
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userRegistrationUniversityPost( universityRegistrationRequestUser: UniversityRegistrationRequestUser, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<User>;

    abstract userRegistrationUniversityPost( universityRegistrationRequestUser: UniversityRegistrationRequestUser, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<User>>;

    abstract userRegistrationUniversityPost( universityRegistrationRequestUser: UniversityRegistrationRequestUser, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<User>>;

    abstract userRegistrationUniversityPost( universityRegistrationRequestUser: UniversityRegistrationRequestUser, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>
}