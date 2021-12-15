import { Component } from '@angular/core'
import { SelfPasswordRequestUser } from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { Router } from '@angular/router'


@Component( {
    selector: 'app-profile-edit-password',
    templateUrl: './profile-edit-password.component.html',
    styleUrls: [ './profile-edit-password.component.scss' ]
} )
export class ProfileEditPasswordComponent
{
    oldPasswordValue: string = ""
    newPasswordValue: string = ""
    newPasswordConfirmValue: string = ""

    constructor( private usersService: UsersService, private router: Router )
    {
    }
    onSubmit(): void
    {
        const request: SelfPasswordRequestUser = {
            old_password: this.oldPasswordValue,
            new_password: this.newPasswordValue
        }
        this.usersService.userProfilePasswordPost( request ).subscribe()
        this.router.navigate( [ '/auth' ] )
    }
}
