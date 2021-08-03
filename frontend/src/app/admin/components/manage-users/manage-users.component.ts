import { Component, OnInit } from '@angular/core'
import { AuthServiceMock } from '@/auth/api/auth.service.mock'
import { ResponseUserAll, TypeCommonName, TypeIdentifier, TypeUserRole, TypeUserType } from '@/auth/models'
import { Observable } from 'rxjs'
import { fixedHeight, footerHeight, headerHeight } from '@/shared/consts'


@Component( {
    selector: 'app-manage-users',
    templateUrl: './manage-users.component.html',
    styleUrls: [ './manage-users.component.scss' ]
} )
export class ManageUsersComponent implements OnInit
{
    users$!: Observable<ResponseUserAll>
    minContainerHeight = fixedHeight
    columnDefs = [
        { field: 'id', sortable: true },
        { field: 'username', sortable: true },
        { field: 'role', sortable: true },
        { field: 'type', sortable: true }
    ]
    headerHeight = headerHeight
    footerHeight = footerHeight

    constructor( private service: AuthServiceMock ) { }

    ngOnInit(): void
    {
        this.users$ = this.service.userAllGet()
    }
}
