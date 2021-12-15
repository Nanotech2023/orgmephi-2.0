import { Component, OnInit } from '@angular/core'
import { Observable } from 'rxjs'
import { ActivatedRoute } from '@angular/router'
import { filter, map } from 'rxjs/operators'


@Component( {
    selector: 'app-confirm-account-request-send',
    templateUrl: './confirm-account-request-send.component.html',
    styleUrls: [ './confirm-account-request-send.component.scss' ]
} )
export class ConfirmAccountRequestSendComponent implements OnInit
{
    email$!: Observable<string>

    constructor( private route: ActivatedRoute ) { }

    ngOnInit()
    {
        this.email$ = this.route.queryParams.pipe( filter( params => params.email ), map( params => params.email ) )
    }
}
