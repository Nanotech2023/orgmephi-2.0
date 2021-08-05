import { Component, ElementRef, OnInit, ViewChild } from '@angular/core'
import { AuthServiceMock } from '@/auth/api/auth.service.mock'
import { ResponseUserAll } from '@/auth/models'
import { Observable } from 'rxjs'
import { fixedHeight } from '@/shared/consts'


@Component( {
    selector: 'app-manage-users',
    templateUrl: './manage-users.component.html',
    styleUrls: [ './manage-users.component.scss' ],
    host: {
        '(document:click)': 'onClick($event)'
    }
} )


export class ManageUsersComponent implements OnInit
{
    users$!: Observable<ResponseUserAll>
    minContainerHeight = fixedHeight
    @ViewChild( 'modal' ) modal!: ElementRef
    columnDefs = [
        { field: 'id', sortable: true, filter: true, headerName: 'ID' },
        { field: 'username', sortable: true, filter: true, headerName: 'Имя пользовтаеля' },
        { field: 'role', sortable: true, filter: true, headerName: 'Роль' },
        { field: 'type', sortable: true, filter: true, headerName: 'Тип регистрации' },
        { headerName: 'Действия', cellRenderer: 'btnCellRenderer' }
    ]
    modalVisible: boolean = false

    constructor( private service: AuthServiceMock ) { }

    ngOnInit(): void
    {
        this.users$ = this.service.userAllGet()
    }

    onClick( $event: any )
    {
        if ( $event.target == this.modal?.nativeElement )
            this.modalVisible = false
    }
}
