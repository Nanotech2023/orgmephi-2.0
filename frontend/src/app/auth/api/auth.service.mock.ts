import { HttpEvent, HttpResponse } from '@angular/common/http'
import { Observable, of } from 'rxjs'
import { Injectable } from '@angular/core'
import { AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'
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
    TypeStudentInfo,
    TypeUserInfo,
    TypeUserRole
} from '@/auth/models'
import { pushPersonalInfo } from '@/auth/store/auth.actions'


@Injectable( {
    providedIn: 'root'
} )
export class AuthServiceMock implements AuthService
{
    constructor( private readonly store: Store<AuthState.State> )
    {
    }

    canConsumeForm( consumes: string[] ): boolean
    {
        return false
    }

    groupAddPost( body: RequestGroupAdd, observe?: "body", reportProgress?: boolean ): Observable<ResponseGroupAdd>
    groupAddPost( body: RequestGroupAdd, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseGroupAdd>>
    groupAddPost( body: RequestGroupAdd, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseGroupAdd>>
    groupAddPost( body: RequestGroupAdd, observe: any, reportProgress: boolean ): Observable<any>
    groupAddPost( body: RequestGroupAdd, observe?: any, reportProgress?: boolean ): Observable<ResponseGroupAdd> | Observable<HttpResponse<ResponseGroupAdd>> | Observable<HttpEvent<ResponseGroupAdd>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    groupAllGet( observe?: "body", reportProgress?: boolean ): Observable<ResponseGroupAll>
    groupAllGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseGroupAll>>
    groupAllGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseGroupAll>>
    groupAllGet( observe: any, reportProgress: boolean ): Observable<any>
    groupAllGet( observe?: any, reportProgress?: boolean ): Observable<ResponseGroupAll> | Observable<HttpResponse<ResponseGroupAll>> | Observable<HttpEvent<ResponseGroupAll>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    groupGroupIdGet( groupId: number, observe?: "body", reportProgress?: boolean ): Observable<ResponseGroup>
    groupGroupIdGet( groupId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseGroup>>
    groupGroupIdGet( groupId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseGroup>>
    groupGroupIdGet( groupId: number, observe: any, reportProgress: boolean ): Observable<any>
    groupGroupIdGet( groupId: number, observe?: any, reportProgress?: boolean ): Observable<ResponseGroup> | Observable<HttpResponse<ResponseGroup>> | Observable<HttpEvent<ResponseGroup>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    groupGroupIdRemovePost( groupId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    groupGroupIdRemovePost( groupId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    groupGroupIdRemovePost( groupId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    groupGroupIdRemovePost( groupId: number, observe: any, reportProgress: boolean ): Observable<any>
    groupGroupIdRemovePost( groupId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    infoCountriesGet( observe?: "body", reportProgress?: boolean ): Observable<ResponseInfoCountries>
    infoCountriesGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseInfoCountries>>
    infoCountriesGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseInfoCountries>>
    infoCountriesGet( observe: any, reportProgress: boolean ): Observable<any>
    infoCountriesGet( observe?: any, reportProgress?: boolean ): Observable<ResponseInfoCountries> | Observable<HttpResponse<ResponseInfoCountries>> | Observable<HttpEvent<ResponseInfoCountries>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    infoUniversitiesGet( observe?: "body", reportProgress?: boolean ): Observable<ResponseInfoUniversities>
    infoUniversitiesGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseInfoUniversities>>
    infoUniversitiesGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseInfoUniversities>>
    infoUniversitiesGet( observe: any, reportProgress: boolean ): Observable<any>
    infoUniversitiesGet( observe?: any, reportProgress?: boolean ): Observable<ResponseInfoUniversities> | Observable<HttpResponse<ResponseInfoUniversities>> | Observable<HttpEvent<ResponseInfoUniversities>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    loginPost( body: RequestLogin, observe?: "body", reportProgress?: boolean ): Observable<ResponseLogin>
    loginPost( body: RequestLogin, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseLogin>>
    loginPost( body: RequestLogin, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseLogin>>
    loginPost( body: RequestLogin, observe: any, reportProgress: boolean ): Observable<any>
    loginPost( body: RequestLogin, observe?: any, reportProgress?: boolean ): Observable<ResponseLogin> | Observable<HttpResponse<ResponseLogin>> | Observable<HttpEvent<ResponseLogin>> | Observable<any>
    {
        const result: ResponseLogin = {}
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

    preregisterPost( observe?: "body", reportProgress?: boolean ): Observable<ResponsePreregister>
    preregisterPost( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponsePreregister>>
    preregisterPost( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponsePreregister>>
    preregisterPost( observe: any, reportProgress: boolean ): Observable<any>
    preregisterPost( observe?: any, reportProgress?: boolean ): Observable<ResponsePreregister> | Observable<HttpResponse<ResponsePreregister>> | Observable<HttpEvent<ResponsePreregister>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    refreshPost( observe?: "body", reportProgress?: boolean ): Observable<ResponseRefresh>
    refreshPost( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseRefresh>>
    refreshPost( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseRefresh>>
    refreshPost( observe: any, reportProgress: boolean ): Observable<any>
    refreshPost( observe?: any, reportProgress?: boolean ): Observable<ResponseRefresh> | Observable<HttpResponse<ResponseRefresh>> | Observable<HttpEvent<ResponseRefresh>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    registerInternalPost( body: TypeAuthCredentials, observe?: "body", reportProgress?: boolean ): Observable<ResponseRegistrationInternal>
    registerInternalPost( body: TypeAuthCredentials, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseRegistrationInternal>>
    registerInternalPost( body: TypeAuthCredentials, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseRegistrationInternal>>
    registerInternalPost( body: TypeAuthCredentials, observe: any, reportProgress: boolean ): Observable<any>
    registerInternalPost( body: TypeAuthCredentials, observe?: any, reportProgress?: boolean ): Observable<ResponseRegistrationInternal> | Observable<HttpResponse<ResponseRegistrationInternal>> | Observable<HttpEvent<ResponseRegistrationInternal>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    registerPost( body: RequestRegistration, observe?: "body", reportProgress?: boolean ): Observable<ResponseRegistration>
    registerPost( body: RequestRegistration, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseRegistration>>
    registerPost( body: RequestRegistration, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseRegistration>>
    registerPost( body: RequestRegistration, observe: any, reportProgress: boolean ): Observable<any>
    registerPost( body: RequestRegistration, observe?: any, reportProgress?: boolean ): Observable<ResponseRegistration> | Observable<HttpResponse<ResponseRegistration>> | Observable<HttpEvent<ResponseRegistration>> | Observable<any>
    {
        const result: TypeUserInfo = {
            username: body.authInfo.email,
            role: TypeUserRole.Participant,
            type: body.registerType,
            id: 12345
        }
        this.store.dispatch( pushPersonalInfo( { personalInfo: body.personalInfo } ) )
        return of( result )
    }

    userAllGet( observe?: "body", reportProgress?: boolean ): Observable<ResponseUserAll>
    userAllGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseUserAll>>
    userAllGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseUserAll>>
    userAllGet( observe: any, reportProgress: boolean ): Observable<any>
    userAllGet( observe?: any, reportProgress?: boolean ): Observable<ResponseUserAll> | Observable<HttpResponse<ResponseUserAll>> | Observable<HttpEvent<ResponseUserAll>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userByGroupGroupIdGet( groupId: number, observe?: "body", reportProgress?: boolean ): Observable<ResponseUserByGroup>
    userByGroupGroupIdGet( groupId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseUserByGroup>>
    userByGroupGroupIdGet( groupId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseUserByGroup>>
    userByGroupGroupIdGet( groupId: number, observe: any, reportProgress: boolean ): Observable<any>
    userByGroupGroupIdGet( groupId: number, observe?: any, reportProgress?: boolean ): Observable<ResponseUserByGroup> | Observable<HttpResponse<ResponseUserByGroup>> | Observable<HttpEvent<ResponseUserByGroup>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfGet( observe?: "body", reportProgress?: boolean ): Observable<ResponseUserSelf>
    userSelfGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseUserSelf>>
    userSelfGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseUserSelf>>
    userSelfGet( observe: any, reportProgress: boolean ): Observable<any>
    userSelfGet( observe?: any, reportProgress?: boolean ): Observable<ResponseUserSelf> | Observable<HttpResponse<ResponseUserSelf>> | Observable<HttpEvent<ResponseUserSelf>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfGroupsGet( observe?: "body", reportProgress?: boolean ): Observable<ResponseUserSelfGroup>
    userSelfGroupsGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseUserSelfGroup>>
    userSelfGroupsGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseUserSelfGroup>>
    userSelfGroupsGet( observe: any, reportProgress: boolean ): Observable<any>
    userSelfGroupsGet( observe?: any, reportProgress?: boolean ): Observable<ResponseUserSelfGroup> | Observable<HttpResponse<ResponseUserSelfGroup>> | Observable<HttpEvent<ResponseUserSelfGroup>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfPasswordPost( body: RequestPasswordSelf, observe?: "body", reportProgress?: boolean ): Observable<any>
    userSelfPasswordPost( body: RequestPasswordSelf, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userSelfPasswordPost( body: RequestPasswordSelf, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userSelfPasswordPost( body: RequestPasswordSelf, observe: any, reportProgress: boolean ): Observable<any>
    userSelfPasswordPost( body: RequestPasswordSelf, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userSelfPersonalGet( observe?: "body", reportProgress?: boolean ): Observable<ResponsePersonalSelf>
    userSelfPersonalGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponsePersonalSelf>>
    userSelfPersonalGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponsePersonalSelf>>
    userSelfPersonalGet( observe: any, reportProgress: boolean ): Observable<any>
    userSelfPersonalGet( observe?: any, reportProgress?: boolean ): Observable<ResponsePersonalSelf> | Observable<HttpResponse<ResponsePersonalSelf>> | Observable<HttpEvent<ResponsePersonalSelf>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userSelfUniversityGet( observe?: "body", reportProgress?: boolean ): Observable<ResponseUniversitySelf>
    userSelfUniversityGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseUniversitySelf>>
    userSelfUniversityGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseUniversitySelf>>
    userSelfUniversityGet( observe: any, reportProgress: boolean ): Observable<any>
    userSelfUniversityGet( observe?: any, reportProgress?: boolean ): Observable<ResponseUniversitySelf> | Observable<HttpResponse<ResponseUniversitySelf>> | Observable<HttpEvent<ResponseUniversitySelf>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdGet( userId: number, observe?: "body", reportProgress?: boolean ): Observable<ResponseUserAdmin>
    userUserIdGet( userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseUserAdmin>>
    userUserIdGet( userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseUserAdmin>>
    userUserIdGet( userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdGet( userId: number, observe?: any, reportProgress?: boolean ): Observable<ResponseUserAdmin> | Observable<HttpResponse<ResponseUserAdmin>> | Observable<HttpEvent<ResponseUserAdmin>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdGroupsAddPost( body: RequestUserGroupsAdd, userId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userUserIdGroupsAddPost( body: RequestUserGroupsAdd, userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userUserIdGroupsAddPost( body: RequestUserGroupsAdd, userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userUserIdGroupsAddPost( body: RequestUserGroupsAdd, userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdGroupsAddPost( body: RequestUserGroupsAdd, userId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdGroupsGet( userId: number, observe?: "body", reportProgress?: boolean ): Observable<ResponseUserAdminGroup>
    userUserIdGroupsGet( userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseUserAdminGroup>>
    userUserIdGroupsGet( userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseUserAdminGroup>>
    userUserIdGroupsGet( userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdGroupsGet( userId: number, observe?: any, reportProgress?: boolean ): Observable<ResponseUserAdminGroup> | Observable<HttpResponse<ResponseUserAdminGroup>> | Observable<HttpEvent<ResponseUserAdminGroup>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdGroupsRemovePost( body: RequestUserGroupsRemove, userId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userUserIdGroupsRemovePost( body: RequestUserGroupsRemove, userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userUserIdGroupsRemovePost( body: RequestUserGroupsRemove, userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userUserIdGroupsRemovePost( body: RequestUserGroupsRemove, userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdGroupsRemovePost( body: RequestUserGroupsRemove, userId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdPasswordPost( body: RequestPasswordAdmin, userId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userUserIdPasswordPost( body: RequestPasswordAdmin, userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userUserIdPasswordPost( body: RequestPasswordAdmin, userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userUserIdPasswordPost( body: RequestPasswordAdmin, userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdPasswordPost( body: RequestPasswordAdmin, userId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdPersonalGet( userId: number, observe?: "body", reportProgress?: boolean ): Observable<ResponsePersonalAdminGet>
    userUserIdPersonalGet( userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponsePersonalAdminGet>>
    userUserIdPersonalGet( userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponsePersonalAdminGet>>
    userUserIdPersonalGet( userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdPersonalGet( userId: number, observe?: any, reportProgress?: boolean ): Observable<ResponsePersonalAdminGet> | Observable<HttpResponse<ResponsePersonalAdminGet>> | Observable<HttpEvent<ResponsePersonalAdminGet>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdPersonalPatch( body: TypePersonalInfo, userId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userUserIdPersonalPatch( body: TypePersonalInfo, userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userUserIdPersonalPatch( body: TypePersonalInfo, userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userUserIdPersonalPatch( body: TypePersonalInfo, userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdPersonalPatch( body: TypePersonalInfo, userId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdRolePut( body: RequestUserRole, userId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userUserIdRolePut( body: RequestUserRole, userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userUserIdRolePut( body: RequestUserRole, userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userUserIdRolePut( body: RequestUserRole, userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdRolePut( body: RequestUserRole, userId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdTypePut( body: RequestUserType, userId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userUserIdTypePut( body: RequestUserType, userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userUserIdTypePut( body: RequestUserType, userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userUserIdTypePut( body: RequestUserType, userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdTypePut( body: RequestUserType, userId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdUniversityGet( userId: number, observe?: "body", reportProgress?: boolean ): Observable<ResponseUniversityAdminGet>
    userUserIdUniversityGet( userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseUniversityAdminGet>>
    userUserIdUniversityGet( userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseUniversityAdminGet>>
    userUserIdUniversityGet( userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdUniversityGet( userId: number, observe?: any, reportProgress?: boolean ): Observable<ResponseUniversityAdminGet> | Observable<HttpResponse<ResponseUniversityAdminGet>> | Observable<HttpEvent<ResponseUniversityAdminGet>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userUserIdUniversityPatch( body: TypeStudentInfo, userId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userUserIdUniversityPatch( body: TypeStudentInfo, userId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userUserIdUniversityPatch( body: TypeStudentInfo, userId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userUserIdUniversityPatch( body: TypeStudentInfo, userId: number, observe: any, reportProgress: boolean ): Observable<any>
    userUserIdUniversityPatch( body: TypeStudentInfo, userId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }
}