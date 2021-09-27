import { Component } from '@angular/core'
import { ProfileStore } from '@/profile/profile.store'
import { Observable } from 'rxjs'
import { UserInfo } from '@api/users/models'


@Component( {
    selector: 'app-profile-view',
    templateUrl: './profile-view.component.html',
    styleUrls: [ './profile-view.component.scss' ],
    providers: [ ProfileStore ]
} )
export class ProfileViewComponent
{
    private userInfo$: Observable<UserInfo | null>

    constructor( private profileStore: ProfileStore )
    {
        this.profileStore.fetch()
        this.userInfo$ = this.profileStore.userInfo$
    }
}