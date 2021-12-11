import { Component } from '@angular/core'
import { ActivatedRoute } from '@angular/router'
import { filter, map } from 'rxjs/operators'
import { Observable } from 'rxjs'


@Component( {
    selector: 'app-reset-password-confirm',
    templateUrl: './reset-password-confirm.component.html',
    styleUrls: [ './reset-password-confirm.component.scss' ]
} )
export class ResetPasswordConfirmComponent
{
    email$!: Observable<string>

    constructor( private route: ActivatedRoute ) { }

    ngOnInit()
    {
        this.email$ = this.route.queryParams.pipe( filter( params => params.email ), map( params => params.email ) )
    }
}
