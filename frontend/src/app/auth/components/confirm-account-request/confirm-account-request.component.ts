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

    constructor( private usersService: UsersService, private router: Router ) { }

    onSubmit(): void
    {
        this.usersService.userRegistrationResendEmailPost( this.emailToReset ).subscribe()
        this.router.navigate( [ "/auth/confirm-account/request-send" ], { queryParams: { email: this.emailToReset } } )
    }
}