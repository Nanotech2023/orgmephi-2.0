import { Component, OnInit } from '@angular/core'
import { UsersService } from '@api/users/users.service'
import { Router } from '@angular/router'


@Component( {
    selector: 'app-confirm-account-request',
    templateUrl: './confirm-account-request.component.html',
    styleUrls: [ './confirm-account-request.component.scss' ]
} )
export class ConfirmAccountRequestComponent
{
    emailToReset: string = ""

    constructor( private usersService: UsersService, private router: Router )
    {
    }

    onSubmit(): void
    {
        this.usersService.userRegistrationForgotEmailPost( this.emailToReset ).subscribe()
        this.router.navigate( [ "/confirm-account/request-send" ], { queryParams: { email: this.emailToReset } } )
    }
}
