import { Component, ElementRef, OnInit, ViewChild } from '@angular/core'
import { ResponseUserAll, TypeRegistrationPersonalInfo } from '@/auth/api/models'
import { Observable } from 'rxjs'
import { fixedHeight } from '@/shared/consts'
import { AuthService } from '@/auth/api/auth.service'
import { AgGridAngular } from 'ag-grid-angular'


@Component( {
    selector: 'app-manage-users',
    templateUrl: './manage-users.component.html',
    styleUrls: [ './manage-users.component.scss' ]
} )


export class ManageUsersComponent implements OnInit
{
    minContainerHeight = fixedHeight
    columnDefs = [
        { field: 'id', sortable: true, filter: true, headerName: 'ID' },
        { field: 'username', sortable: true, filter: true, headerName: 'Имя пользовтаеля' },
        { field: 'role', sortable: true, filter: true, headerName: 'Роль' },
        { field: 'type', sortable: true, filter: true, headerName: 'Тип регистрации' },
        { headerName: 'Действия' }
    ]
    modalVisible: boolean = false
    @ViewChild( 'table_users' ) agGrid!: AgGridAngular
    users$!: Observable<ResponseUserAll>

    constructor( private service: AuthService ) { }

    ngOnInit(): void
    {
        this.users$ = this.service.userAllGet()
    }

    onNewUserAdded( userInfo: TypeRegistrationPersonalInfo )
    {
        this.agGrid.api.addItems( [
            {
                type: 'School',
                username: userInfo.first_name,
                role: 'Participant'
            }
        ] )
    }
}
