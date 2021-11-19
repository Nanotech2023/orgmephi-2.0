import { Component } from '@angular/core'
import { ProfileStore } from '@/profile/profile.store'
import { Observable } from 'rxjs'
import {
    UserInfo,
    SchoolInfo,
    DocumentRF,
    LocationRussia,
    UserLimitations,
    GenderEnum,
    DocumentTypeEnum
} from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { getDocumentDisplay, getGenderDisplay } from '@/shared/displayUtils'


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


    readonly genders: GenderEnum[] = [ GenderEnum.Male, GenderEnum.Female ]
    mobNumberPattern = "^((\\+91-?)|0)?[0-9]{10}$"

    constructor( private profileStore: ProfileStore, private usersService: UsersService )
    {
        this.profileStore.fetch()
        this.viewModel$ = this.profileStore.viewModel$
    }

    updateUserInfo( userInfo: UserInfo ): void
    {
        this.profileStore.updateUserInfo( userInfo )
    }

    updateSchoolInfo( schoolInfo: SchoolInfo ): void
    {
        this.profileStore.updateSchoolInfo( schoolInfo )
    }

    download(): void
    {
        this.usersService.userProfileCardGet().subscribe( data => this.downloadFile( data ) )
    }

    getGenderDisplay( genderEnum: GenderEnum ): string
    {
        return getGenderDisplay( genderEnum )
    }

    downloadFile( data: Blob ): void
    {
        const blob = new Blob( [ data ], { type: 'application/pdf' } )
        const url = window.URL.createObjectURL( blob )
        window.open( url )
    }

}