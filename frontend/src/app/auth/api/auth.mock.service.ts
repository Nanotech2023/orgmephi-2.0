import { HttpEvent, HttpResponse } from '@angular/common/http'
import { Observable, of } from 'rxjs'
import { Injectable } from '@angular/core'
import { AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'
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
    RoleType,
    StudentInfo,
    StudentInfoUpdate,
    UpdateGroups,
    UserList,
    UserRole
} from '@/auth/models'
import { IAuthService } from '@/auth/api/auth.service.int'
import { pushPersonalInfo } from '@/auth/store/auth.actions'


@Injectable( {
    providedIn: 'root'
} )
export class AuthServiceMock implements IAuthService
{
    constructor( private readonly store: Store<AuthState.State> )
    {
    }

    canConsumeForm( consumes: string[] ): boolean
    {
        return false
    }

    groupAddPost( body: AddGroup, observe?: "body", reportProgress?: boolean ): Observable<GroupType>
    groupAddPost( body: AddGroup, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<GroupType>>
    groupAddPost( body: AddGroup, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<GroupType>>
    groupAddPost( body: AddGroup, observe: any, reportProgress: boolean ): Observable<any>
    groupAddPost( body: AddGroup, observe?: any, reportProgress?: boolean ): Observable<GroupType> | Observable<HttpResponse<GroupType>> | Observable<HttpEvent<GroupType>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    groupAllGet( observe?: "body", reportProgress?: boolean ): Observable<GroupList>
    groupAllGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<GroupList>>
    groupAllGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<GroupList>>
    groupAllGet( observe: any, reportProgress: boolean ): Observable<any>
    groupAllGet( observe?: any, reportProgress?: boolean ): Observable<GroupList> | Observable<HttpResponse<GroupList>> | Observable<HttpEvent<GroupList>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    groupIdDeletePost( body: AddGroup, id: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    groupIdDeletePost( body: AddGroup, id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    groupIdDeletePost( body: AddGroup, id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    groupIdDeletePost( body: AddGroup, id: number, observe: any, reportProgress: boolean ): Observable<any>
    groupIdDeletePost( body: AddGroup, id: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    groupIdGet( id: number, observe?: "body", reportProgress?: boolean ): Observable<GroupType>
    groupIdGet( id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<GroupType>>
    groupIdGet( id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<GroupType>>
    groupIdGet( id: number, observe: any, reportProgress: boolean ): Observable<any>
    groupIdGet( id: number, observe?: any, reportProgress?: boolean ): Observable<GroupType> | Observable<HttpResponse<GroupType>> | Observable<HttpEvent<GroupType>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    infoCountriesGet( observe?: "body", reportProgress?: boolean ): Observable<GetCountriesResponse>
    infoCountriesGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<GetCountriesResponse>>
    infoCountriesGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<GetCountriesResponse>>
    infoCountriesGet( observe: any, reportProgress: boolean ): Observable<any>
    infoCountriesGet( observe?: any, reportProgress?: boolean ): Observable<GetCountriesResponse> | Observable<HttpResponse<GetCountriesResponse>> | Observable<HttpEvent<GetCountriesResponse>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    infoUniversitiesGet( observe?: "body", reportProgress?: boolean ): Observable<GetUniversitiesResponse>
    infoUniversitiesGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<GetUniversitiesResponse>>
    infoUniversitiesGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<GetUniversitiesResponse>>
    infoUniversitiesGet( observe: any, reportProgress: boolean ): Observable<any>
    infoUniversitiesGet( observe?: any, reportProgress?: boolean ): Observable<GetUniversitiesResponse> | Observable<HttpResponse<GetUniversitiesResponse>> | Observable<HttpEvent<GetUniversitiesResponse>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    loginPost( body: Authentication, observe?: "body", reportProgress?: boolean ): Observable<AuthResponse>
    loginPost( body: Authentication, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<AuthResponse>>
    loginPost( body: Authentication, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<AuthResponse>>
    loginPost( body: Authentication, observe: any, reportProgress: boolean ): Observable<any>
    loginPost( body: Authentication, observe?: any, reportProgress?: boolean ): Observable<AuthResponse> | Observable<HttpResponse<AuthResponse>> | Observable<HttpEvent<AuthResponse>> | Observable<any>
    {
        const result: AuthResponse = { csrfAccessToken: "access", csrfRefreshToken: "refresh" }
        return of( result )
    }

    logoutPost( observe?: "body", reportProgress?: boolean ): Observable<any>
    logoutPost( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    logoutPost( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    logoutPost( observe: any, reportProgress: boolean ): Observable<any>
    logoutPost( observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    preregisterPost( observe?: "body", reportProgress?: boolean ): Observable<RegisterConfirm>
    preregisterPost( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<RegisterConfirm>>
    preregisterPost( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<RegisterConfirm>>
    preregisterPost( observe: any, reportProgress: boolean ): Observable<any>
    preregisterPost( observe?: any, reportProgress?: boolean ): Observable<RegisterConfirm> | Observable<HttpResponse<RegisterConfirm>> | Observable<HttpEvent<RegisterConfirm>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    refreshPost( observe?: "body", reportProgress?: boolean ): Observable<AuthResponse>
    refreshPost( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<AuthResponse>>
    refreshPost( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<AuthResponse>>
    refreshPost( observe: any, reportProgress: boolean ): Observable<any>
    refreshPost( observe?: any, reportProgress?: boolean ): Observable<AuthResponse> | Observable<HttpResponse<AuthResponse>> | Observable<HttpEvent<AuthResponse>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    registerInternalPost( body: RegisterAuthInfo, observe?: "body", reportProgress?: boolean ): Observable<CommonUserInfo>
    registerInternalPost( body: RegisterAuthInfo, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonUserInfo>>
    registerInternalPost( body: RegisterAuthInfo, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonUserInfo>>
    registerInternalPost( body: RegisterAuthInfo, observe: any, reportProgress: boolean ): Observable<any>
    registerInternalPost( body: RegisterAuthInfo, observe?: any, reportProgress?: boolean ): Observable<CommonUserInfo> | Observable<HttpResponse<CommonUserInfo>> | Observable<HttpEvent<CommonUserInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    registerPost( body: Registration, observe?: "body", reportProgress?: boolean ): Observable<CommonUserInfo>
    registerPost( body: Registration, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonUserInfo>>
    registerPost( body: Registration, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonUserInfo>>
    registerPost( body: Registration, observe: any, reportProgress: boolean ): Observable<any>
    registerPost( body: Registration, observe?: any, reportProgress?: boolean ): Observable<CommonUserInfo> | Observable<HttpResponse<CommonUserInfo>> | Observable<HttpEvent<CommonUserInfo>> | Observable<any>
    {
        const result: CommonUserInfo = {
            username: body.authInfo.email,
            role: RoleType.Participant,
            type: body.registerType,
            id: 12345
        }
        this.store.dispatch( pushPersonalInfo( { personalInfo: body.personalInfo } ) )
        return of( result )
    }

    userAllGet( observe?: "body", reportProgress?: boolean ): Observable<UserList>
    userAllGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UserList>>
    userAllGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UserList>>
    userAllGet( observe: any, reportProgress: boolean ): Observable<any>
    userAllGet( observe?: any, reportProgress?: boolean ): Observable<UserList> | Observable<HttpResponse<UserList>> | Observable<HttpEvent<UserList>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userByGroupIdGet( id: number, observe?: "body", reportProgress?: boolean ): Observable<UserList>
    userByGroupIdGet( id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UserList>>
    userByGroupIdGet( id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UserList>>
    userByGroupIdGet( id: number, observe: any, reportProgress: boolean ): Observable<any>
    userByGroupIdGet( id: number, observe?: any, reportProgress?: boolean ): Observable<UserList> | Observable<HttpResponse<UserList>> | Observable<HttpEvent<UserList>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userIdGet( id: number, observe?: "body", reportProgress?: boolean ): Observable<CommonUserInfo>
    userIdGet( id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonUserInfo>>
    userIdGet( id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonUserInfo>>
    userIdGet( id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdGet( id: number, observe?: any, reportProgress?: boolean ): Observable<CommonUserInfo> | Observable<HttpResponse<CommonUserInfo>> | Observable<HttpEvent<CommonUserInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userIdGroupsAddPost( body: UpdateGroups, id: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userIdGroupsAddPost( body: UpdateGroups, id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userIdGroupsAddPost( body: UpdateGroups, id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userIdGroupsAddPost( body: UpdateGroups, id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdGroupsAddPost( body: UpdateGroups, id: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userIdGroupsGet( id: number, observe?: "body", reportProgress?: boolean ): Observable<GroupList>
    userIdGroupsGet( id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<GroupList>>
    userIdGroupsGet( id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<GroupList>>
    userIdGroupsGet( id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdGroupsGet( id: number, observe?: any, reportProgress?: boolean ): Observable<GroupList> | Observable<HttpResponse<GroupList>> | Observable<HttpEvent<GroupList>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userIdGroupsRemovePost( body: UpdateGroups, id: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userIdGroupsRemovePost( body: UpdateGroups, id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userIdGroupsRemovePost( body: UpdateGroups, id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userIdGroupsRemovePost( body: UpdateGroups, id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdGroupsRemovePost( body: UpdateGroups, id: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userIdPasswordPost( body: ChangePasswordAdmin, id: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userIdPasswordPost( body: ChangePasswordAdmin, id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userIdPasswordPost( body: ChangePasswordAdmin, id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userIdPasswordPost( body: ChangePasswordAdmin, id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdPasswordPost( body: ChangePasswordAdmin, id: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userIdPersonalGet( id: number, observe?: "body", reportProgress?: boolean ): Observable<PersonalInfo>
    userIdPersonalGet( id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<PersonalInfo>>
    userIdPersonalGet( id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<PersonalInfo>>
    userIdPersonalGet( id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdPersonalGet( id: number, observe?: any, reportProgress?: boolean ): Observable<PersonalInfo> | Observable<HttpResponse<PersonalInfo>> | Observable<HttpEvent<PersonalInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userIdPersonalPatch( body: PersonalInfoUpdate, id: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userIdPersonalPatch( body: PersonalInfoUpdate, id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userIdPersonalPatch( body: PersonalInfoUpdate, id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userIdPersonalPatch( body: PersonalInfoUpdate, id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdPersonalPatch( body: PersonalInfoUpdate, id: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userIdRolePut( body: UserRole, id: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userIdRolePut( body: UserRole, id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userIdRolePut( body: UserRole, id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userIdRolePut( body: UserRole, id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdRolePut( body: UserRole, id: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userIdTypePut( body: AccountType, id: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userIdTypePut( body: AccountType, id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userIdTypePut( body: AccountType, id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userIdTypePut( body: AccountType, id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdTypePut( body: AccountType, id: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userIdUniversityGet( id: number, observe?: "body", reportProgress?: boolean ): Observable<StudentInfo>
    userIdUniversityGet( id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<StudentInfo>>
    userIdUniversityGet( id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<StudentInfo>>
    userIdUniversityGet( id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdUniversityGet( id: number, observe?: any, reportProgress?: boolean ): Observable<StudentInfo> | Observable<HttpResponse<StudentInfo>> | Observable<HttpEvent<StudentInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userIdUniversityPatch( body: StudentInfoUpdate, id: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userIdUniversityPatch( body: StudentInfoUpdate, id: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userIdUniversityPatch( body: StudentInfoUpdate, id: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userIdUniversityPatch( body: StudentInfoUpdate, id: number, observe: any, reportProgress: boolean ): Observable<any>
    userIdUniversityPatch( body: StudentInfoUpdate, id: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userSelfGet( observe?: "body", reportProgress?: boolean ): Observable<CommonUserInfo>
    userSelfGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonUserInfo>>
    userSelfGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonUserInfo>>
    userSelfGet( observe: any, reportProgress: boolean ): Observable<any>
    userSelfGet( observe?: any, reportProgress?: boolean ): Observable<CommonUserInfo> | Observable<HttpResponse<CommonUserInfo>> | Observable<HttpEvent<CommonUserInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfGroupsGet( observe?: "body", reportProgress?: boolean ): Observable<GroupList>
    userSelfGroupsGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<GroupList>>
    userSelfGroupsGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<GroupList>>
    userSelfGroupsGet( observe: any, reportProgress: boolean ): Observable<any>
    userSelfGroupsGet( observe?: any, reportProgress?: boolean ): Observable<GroupList> | Observable<HttpResponse<GroupList>> | Observable<HttpEvent<GroupList>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfPasswordPost( body: ChangePassword, observe?: "body", reportProgress?: boolean ): Observable<any>
    userSelfPasswordPost( body: ChangePassword, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userSelfPasswordPost( body: ChangePassword, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userSelfPasswordPost( body: ChangePassword, observe: any, reportProgress: boolean ): Observable<any>
    userSelfPasswordPost( body: ChangePassword, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userSelfPersonalGet( observe?: "body", reportProgress?: boolean ): Observable<PersonalInfo>
    userSelfPersonalGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<PersonalInfo>>
    userSelfPersonalGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<PersonalInfo>>
    userSelfPersonalGet( observe: any, reportProgress: boolean ): Observable<any>
    userSelfPersonalGet( observe?: any, reportProgress?: boolean ): Observable<PersonalInfo> | Observable<HttpResponse<PersonalInfo>> | Observable<HttpEvent<PersonalInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfUniversityGet( observe?: "body", reportProgress?: boolean ): Observable<StudentInfo>
    userSelfUniversityGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<StudentInfo>>
    userSelfUniversityGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<StudentInfo>>
    userSelfUniversityGet( observe: any, reportProgress: boolean ): Observable<any>
    userSelfUniversityGet( observe?: any, reportProgress?: boolean ): Observable<StudentInfo> | Observable<HttpResponse<StudentInfo>> | Observable<HttpEvent<StudentInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }
}