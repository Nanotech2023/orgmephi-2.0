import { Component, OnInit } from '@angular/core'
import { UsersService } from '@api/users/users.service'
import { UserInfo } from '@api/users/models'
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
    editUserPersonalInfo!: Observable<UserInfo>
    currentStage: number
    totalStages = 2

    constructor( private authService: UsersService, private readonly store: Store<AuthState.State> )
    {
        this.currentStage = 0
    }

    ngOnInit(): void
    {
        this.editUserPersonalInfo = this.store.select( AuthSelectors.selectUserInfo )
    }

    onSubmit( editUserPersonalInfo: UserInfo ): void
    {
        this.authService.userProfilePersonalPatch( editUserPersonalInfo )
    }
}
