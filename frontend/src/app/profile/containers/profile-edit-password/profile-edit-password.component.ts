import { Component, OnInit } from '@angular/core'
import { Observable } from 'rxjs'
import { SelfPasswordRequestUser } from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { Store } from '@ngrx/store'
import { AuthActions, AuthSelectors, AuthState } from '@/auth/store'
import { Router } from '@angular/router'


@Component( {
    selector: 'app-profile-edit-password',
    templateUrl: './profile-edit-password.component.html',
    styleUrls: [ './profile-edit-password.component.scss' ]
} )
export class ProfileEditPasswordComponent implements OnInit
{
    isPrivileged$!: Observable<boolean>
    oldPasswordValue: string = ""
    newPasswordValue: string = ""
    newPasswordConfirmValue: string = ""

    constructor( private usersService: UsersService, private router: Router, private store: Store<AuthState.State> )
    {
    }

    ngOnInit(): void
    {
        this.isPrivileged$ = this.store.select( AuthSelectors.selectIsPrivileged )
    }

    logoutButtonClick(): void
    {
        this.store.dispatch( AuthActions.logoutRequest() )
    }

    onSubmit(): void
    {
        const request: SelfPasswordRequestUser = {
            old_password: this.oldPasswordValue,
            new_password: this.newPasswordValue
        }
        this.usersService.userProfilePasswordPost( request ).subscribe()
        this.router.navigate( [ '/login' ] )
    }
}
