import { Component } from '@angular/core'
import { ActivatedRoute } from '@angular/router'
import { filter, map } from 'rxjs/operators'
import { Observable } from 'rxjs'


@Component( {
    selector: 'app-reset-password-request-send',
    templateUrl: './reset-password-request-send.component.html',
    styleUrls: [ './reset-password-request-send.component.scss' ]
} )
export class ResetPasswordRequestSendComponent
{
    email$!: Observable<string>

    constructor( private route: ActivatedRoute ) { }

    ngOnInit(): void
    {
        this.email$ = this.route.queryParams.pipe( filter( params => params.email ), map( params => params.email ) )
    }
}
