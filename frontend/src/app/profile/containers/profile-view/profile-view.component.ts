import { Component } from '@angular/core'
import { ProfileStore } from '@/profile/profile.store'
import { Observable } from 'rxjs'
import { UserInfo, SchoolInfo } from '@api/users/models'
import { LoadingState } from '@/shared/callState'


@Component( {
    selector: 'app-profile-view',
    templateUrl: './profile-view.component.html',
    styleUrls: [ './profile-view.component.scss' ],
    providers: [ ProfileStore ]
} )
export class ProfileViewComponent
{
    viewModel$: Observable<{ loading: boolean; error: string | null, userProfileUnfilled: string, userInfo: UserInfo, schoolInfo: SchoolInfo }>

    constructor( private profileStore: ProfileStore )
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
}