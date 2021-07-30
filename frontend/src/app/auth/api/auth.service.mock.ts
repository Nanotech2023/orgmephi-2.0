import { Injectable } from '@angular/core'
import { AuthService } from '@/auth/api/auth.service'
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
    TypeUserInfo,
    TypeUserRole
} from '@/auth/api/models'
import { HttpEvent, HttpParams, HttpResponse } from '@angular/common/http'
import { Observable, of } from 'rxjs'
import { pushPersonalInfo } from '@/auth/store/auth.actions'
import { AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'


@Injectable( {
    providedIn: 'root'
} )
export class AuthServiceMock implements AuthService
{
    constructor( private readonly store: Store<AuthState.State> )
    {
    }

    addToHttpParams( httpParams: HttpParams, value: any, key?: string ): HttpParams
    {
        throw new Error( 'not implemented' )
    }

    addToHttpParamsRecursive( httpParams: HttpParams, value?: any, key?: string ): HttpParams
    {
        throw new Error( 'not implemented' )
    }

    groupAddPost( requestGroupAdd: RequestGroupAdd, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeGroup>
    groupAddPost( requestGroupAdd: RequestGroupAdd, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypeGroup>>
    groupAddPost( requestGroupAdd: RequestGroupAdd, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypeGroup>>
    groupAddPost( requestGroupAdd: RequestGroupAdd, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    groupAddPost( requestGroupAdd: RequestGroupAdd, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeGroup> | Observable<HttpResponse<TypeGroup>> | Observable<HttpEvent<TypeGroup>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    groupAllGet( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseGroupAll>
    groupAllGet( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<ResponseGroupAll>>
    groupAllGet( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<ResponseGroupAll>>
    groupAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    groupAllGet( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseGroupAll> | Observable<HttpResponse<ResponseGroupAll>> | Observable<HttpEvent<ResponseGroupAll>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    groupGroupIdGet( groupId: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeGroup>
    groupGroupIdGet( groupId: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypeGroup>>
    groupGroupIdGet( groupId: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypeGroup>>
    groupGroupIdGet( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    groupGroupIdGet( groupId: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeGroup> | Observable<HttpResponse<TypeGroup>> | Observable<HttpEvent<TypeGroup>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    groupGroupIdRemovePost( groupId: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    groupGroupIdRemovePost( groupId: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    groupGroupIdRemovePost( groupId: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    groupGroupIdRemovePost( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    groupGroupIdRemovePost( groupId: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    infoCountriesGet( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseInfoCountries>
    infoCountriesGet( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<ResponseInfoCountries>>
    infoCountriesGet( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<ResponseInfoCountries>>
    infoCountriesGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    infoCountriesGet( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseInfoCountries> | Observable<HttpResponse<ResponseInfoCountries>> | Observable<HttpEvent<ResponseInfoCountries>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    infoUniversitiesGet( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseInfoUniversities>
    infoUniversitiesGet( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<ResponseInfoUniversities>>
    infoUniversitiesGet( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<ResponseInfoUniversities>>
    infoUniversitiesGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    infoUniversitiesGet( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseInfoUniversities> | Observable<HttpResponse<ResponseInfoUniversities>> | Observable<HttpEvent<ResponseInfoUniversities>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    loginPost( requestLogin: RequestLogin, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeCSRFPair>
    loginPost( requestLogin: RequestLogin, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypeCSRFPair>>
    loginPost( requestLogin: RequestLogin, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypeCSRFPair>>
    loginPost( requestLogin: RequestLogin, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    loginPost( requestLogin: RequestLogin, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeCSRFPair> | Observable<HttpResponse<TypeCSRFPair>> | Observable<HttpEvent<TypeCSRFPair>> | Observable<any>
    {
        const result: TypeCSRFPair = {
            csrf_access_token: 'access token value',
            csrf_refresh_token: 'refresh token value'
        }
        return of( result )
    }

    logoutPost( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>
    logoutPost( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpResponse<any>>
    logoutPost( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<HttpEvent<any>>
    logoutPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any>
    logoutPost( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: undefined } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    preregisterPost( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypePreregisterInfo>
    preregisterPost( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypePreregisterInfo>>
    preregisterPost( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypePreregisterInfo>>
    preregisterPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    preregisterPost( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypePreregisterInfo> | Observable<HttpResponse<TypePreregisterInfo>> | Observable<HttpEvent<TypePreregisterInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    refreshPost( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeCSRFPair>
    refreshPost( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypeCSRFPair>>
    refreshPost( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypeCSRFPair>>
    refreshPost( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    refreshPost( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeCSRFPair> | Observable<HttpResponse<TypeCSRFPair>> | Observable<HttpEvent<TypeCSRFPair>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    registerInternalPost( body: TypeAuthCredentials, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeUserInfo>
    registerInternalPost( body: TypeAuthCredentials, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypeUserInfo>>
    registerInternalPost( body: TypeAuthCredentials, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypeUserInfo>>
    registerInternalPost( body: TypeAuthCredentials, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    registerInternalPost( body: TypeAuthCredentials, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeUserInfo> | Observable<HttpResponse<TypeUserInfo>> | Observable<HttpEvent<TypeUserInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    registerPost( requestRegistration: RequestRegistration, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeUserInfo>
    registerPost( requestRegistration: RequestRegistration, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypeUserInfo>>
    registerPost( requestRegistration: RequestRegistration, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypeUserInfo>>
    registerPost( requestRegistration: RequestRegistration, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    registerPost( requestRegistration: RequestRegistration, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeUserInfo> | Observable<HttpResponse<TypeUserInfo>> | Observable<HttpEvent<TypeUserInfo>> | Observable<any>
    {
        const result: TypeUserInfo = {
            username: requestRegistration.auth_info.email,
            role: TypeUserRole.Participant,
            type: requestRegistration.register_type,
            id: 12345
        }
        this.store.dispatch( pushPersonalInfo( { personalInfo: requestRegistration.personal_info } ) )
        return of( result )
    }

    userAllGet( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseUserAll>
    userAllGet( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<ResponseUserAll>>
    userAllGet( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<ResponseUserAll>>
    userAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userAllGet( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseUserAll> | Observable<HttpResponse<ResponseUserAll>> | Observable<HttpEvent<ResponseUserAll>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userByGroupGroupIdGet( groupId: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseUserByGroup>
    userByGroupGroupIdGet( groupId: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<ResponseUserByGroup>>
    userByGroupGroupIdGet( groupId: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<ResponseUserByGroup>>
    userByGroupGroupIdGet( groupId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userByGroupGroupIdGet( groupId: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseUserByGroup> | Observable<HttpResponse<ResponseUserByGroup>> | Observable<HttpEvent<ResponseUserByGroup>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfGet( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeUserInfo>
    userSelfGet( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypeUserInfo>>
    userSelfGet( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypeUserInfo>>
    userSelfGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userSelfGet( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeUserInfo> | Observable<HttpResponse<TypeUserInfo>> | Observable<HttpEvent<TypeUserInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfGroupsGet( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseUserSelfGroup>
    userSelfGroupsGet( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<ResponseUserSelfGroup>>
    userSelfGroupsGet( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<ResponseUserSelfGroup>>
    userSelfGroupsGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userSelfGroupsGet( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseUserSelfGroup> | Observable<HttpResponse<ResponseUserSelfGroup>> | Observable<HttpEvent<ResponseUserSelfGroup>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userSelfPasswordPost( requestPasswordSelf: RequestPasswordSelf, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userSelfPersonalGet( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypePersonalInfo>
    userSelfPersonalGet( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypePersonalInfo>>
    userSelfPersonalGet( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypePersonalInfo>>
    userSelfPersonalGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userSelfPersonalGet( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypePersonalInfo> | Observable<HttpResponse<TypePersonalInfo>> | Observable<HttpEvent<TypePersonalInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfUniversityGet( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypePersonalInfo>
    userSelfUniversityGet( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypePersonalInfo>>
    userSelfUniversityGet( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypePersonalInfo>>
    userSelfUniversityGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userSelfUniversityGet( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypePersonalInfo> | Observable<HttpResponse<TypePersonalInfo>> | Observable<HttpEvent<TypePersonalInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdGet( userId: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeUserInfo>
    userUserIdGet( userId: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypeUserInfo>>
    userUserIdGet( userId: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypeUserInfo>>
    userUserIdGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdGet( userId: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeUserInfo> | Observable<HttpResponse<TypeUserInfo>> | Observable<HttpEvent<TypeUserInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdGroupsAddPost( userId: number, requestUserGroupsAdd: RequestUserGroupsAdd, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdGroupsGet( userId: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseUserAdminGroup>
    userUserIdGroupsGet( userId: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<ResponseUserAdminGroup>>
    userUserIdGroupsGet( userId: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<ResponseUserAdminGroup>>
    userUserIdGroupsGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdGroupsGet( userId: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ResponseUserAdminGroup> | Observable<HttpResponse<ResponseUserAdminGroup>> | Observable<HttpEvent<ResponseUserAdminGroup>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdGroupsRemovePost( userId: number, requestUserGroupsRemove: RequestUserGroupsRemove, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdPasswordPost( userId: number, requestPasswordAdmin: RequestPasswordAdmin, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdPersonalGet( userId: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypePersonalInfo>
    userUserIdPersonalGet( userId: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypePersonalInfo>>
    userUserIdPersonalGet( userId: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypePersonalInfo>>
    userUserIdPersonalGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdPersonalGet( userId: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypePersonalInfo> | Observable<HttpResponse<TypePersonalInfo>> | Observable<HttpEvent<TypePersonalInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdPersonalPatch( userId: number, body: TypePersonalInfo, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdRolePut( userId: number, requestUserRole: RequestUserRole, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdTypePut( userId: number, requestUserType: RequestUserType, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdUniversityGet( userId: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeStudentInfo>
    userUserIdUniversityGet( userId: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TypeStudentInfo>>
    userUserIdUniversityGet( userId: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TypeStudentInfo>>
    userUserIdUniversityGet( userId: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdUniversityGet( userId: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TypeStudentInfo> | Observable<HttpResponse<TypeStudentInfo>> | Observable<HttpEvent<TypeStudentInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userUserIdUniversityPatch( userId: number, body: TypeStudentInfo, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }
}