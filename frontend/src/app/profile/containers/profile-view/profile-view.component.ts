import { Component } from '@angular/core'
import { ProfileStore } from '@/profile/profile.store'
import { Observable } from 'rxjs'
import { UserInfo, SchoolInfo, DocumentRF, LocationRussia, UserLimitations } from '@api/users/models'
import { LoadingState } from '@/shared/callState'
import { UsersService } from '@api/users/users.service'


@Component( {
    selector: 'app-profile-view',
    templateUrl: './profile-view.component.html',
    styleUrls: [ './profile-view.component.scss' ],
    providers: [ ProfileStore ]
} )
export class ProfileViewComponent
{
    viewModel$: Observable<{
        loading: boolean; error: string | null, userProfileUnfilled: string,
        userInfo: UserInfo,
        userInfoDocument: DocumentRF,
        userInfoDwelling: LocationRussia,
        userInfoLimitations: UserLimitations,
        schoolInfo: SchoolInfo
    }>

    readonly genders: ( "Male" | "Female" )[] = [ UserInfo.GenderEnum.Male, UserInfo.GenderEnum.Female ]

    constructor( private profileStore: ProfileStore, private usersService: UsersService )
    {
        this.profileStore.fetch()
        this.viewModel$ = this.profileStore.viewModel$
    }

    updateUserInfo( userInfo: UserInfo )
    {
        this.profileStore.updateUserInfo( userInfo )
    }

    updateSchoolInfo( schoolInfo: SchoolInfo )
    {
        this.profileStore.updateSchoolInfo( schoolInfo )
    }

    download()
    {
        this.usersService.userProfileCardGet().subscribe( data => this.downloadFile( data ) )
    }

    downloadFile( data: Blob )
    {
        const blob = new Blob( [ data ], { type: 'application/pdf' } )
        const url = window.URL.createObjectURL( blob )
        window.open( url )
    }
}