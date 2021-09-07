import { Component, OnInit } from '@angular/core'
import { AuthService } from '@/auth/api/auth.service'
import { UserInfo, UserInfoRestrictedInput } from '@/auth/api/models'
import { Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { Observable } from 'rxjs'


@Component( {
    selector: 'app-participant-registration-form',
    templateUrl: './participant-registration-form.component.html',
    styleUrls: [ './participant-registration-form.component.scss' ]
} )
export class ParticipantRegistrationFormComponent implements OnInit
{
    // @ts-ignore
    userPersonalInfo: UserInfoRestrictedInput
    currentStage: number
    totalStages = 2
    private x: Observable<UserInfo | null>

    constructor( private authService: AuthService, private readonly store: Store<AuthState.State> )
    {
        this.currentStage = 0
    }

    ngOnInit(): void
    {
        this.authService.userProfilePersonalPatch()
        this.x = this.store.select( AuthSelectors.selectUserInfo )

        let y
        this.userPersonalInfo = {
            document: y
        }
    }
}
